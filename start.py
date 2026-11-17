"""รันเว็บแอปแผนที่ ใช้ได้ทั้ง macOS และ Windows

วิธีใช้ (รันจากโฟลเดอร์หลักของโปรเจกต์):
    python start.py                     รันทุก service
    python start.py python frontend     รันเฉพาะ service ที่ระบุ (python, rust, frontend)
    python start.py test                รัน test ของ backend

บน macOS ให้พิมพ์ python3 แทน python
กด Ctrl+C ในหน้าต่างเดิมเมื่อต้องการปิด

For maintainers: standard library only, so it runs before anything is installed.
It prepares each service first (venv + pip, npm install, cargo build), then starts
them as child processes and stops all of them together. Every OS-specific detail
(venv layout, process-tree shutdown) lives in this file.
"""

import os
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON_DIR = ROOT / "backend-python"
RUST_DIR = ROOT / "backend-rust"
FRONTEND_DIR = ROOT / "frontend"

IS_WINDOWS = os.name == "nt"
HOST = "127.0.0.1"  # local only: binding wider makes Windows Firewall prompt for admin approval
SERVICES = ("python", "rust", "frontend")
PORTS = {"python": 8000, "rust": 8080, "frontend": 5173}
LABELS = {
    "python": "Backend Python (FastAPI)",
    "rust": "Backend Rust (Axum)",
    "frontend": "Frontend (Vite)",
}
RUST_GUIDE = "backend-rust/README.md"
SHUTDOWN_GRACE_SECONDS = 5


class Stop(Exception):
    """Raised with a Thai message that tells the user what went wrong and what to do."""


def say(text=""):
    print(text, flush=True)


def heading(text):
    say()
    say(f"== {text}")


# ---------------------------------------------------------------- tools on this machine


def venv_python():
    folder = "Scripts" if IS_WINDOWS else "bin"
    name = "python.exe" if IS_WINDOWS else "python"
    return PYTHON_DIR / "venv" / folder / name


def find_cargo():
    found = shutil.which("cargo")
    if found:
        return found
    # rustup installs here; a terminal opened before the install does not have it on PATH yet.
    fallback = Path.home() / ".cargo" / "bin" / ("cargo.exe" if IS_WINDOWS else "cargo")
    return str(fallback) if fallback.exists() else None


def find_node():
    """Return the path to node, or raise Stop when it is missing or too old for Vite."""
    node = shutil.which("node")
    npm = shutil.which("npm")
    install_help = (
        "ติดตั้งรุ่น LTS จาก https://nodejs.org (กดถัดไปจนจบ) "
        "แล้วปิด terminal เปิดใหม่ก่อนรันคำสั่งนี้อีกครั้ง"
    )
    if not node or not npm:
        raise Stop(f"ไม่พบ Node.js ในเครื่อง ซึ่งจำเป็นสำหรับหน้าเว็บแผนที่\n{install_help}")

    version = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip()
    try:
        major = int(version.lstrip("v").split(".")[0])
    except ValueError:
        major = 0
    if major < 18 or major == 19:  # Vite 5 supports Node 18 and 20+
        raise Stop(f"Node.js ในเครื่องเป็นรุ่น {version} ซึ่งเก่าเกินไป ต้องใช้รุ่น 20 ขึ้นไป\n{install_help}")
    return node


def port_in_use(port, addresses=("127.0.0.1", "::1")):
    for address in addresses:
        try:
            with socket.create_connection((address, port), timeout=0.5):
                return True
        except OSError:
            continue
    return False


def check_ports_free(services):
    busy = [name for name in services if port_in_use(PORTS[name])]
    if not busy:
        return
    lines = [f"  พอร์ต {PORTS[name]} ({LABELS[name]})" for name in busy]
    raise Stop(
        "มีโปรแกรมอื่นใช้พอร์ตเหล่านี้อยู่แล้ว:\n"
        + "\n".join(lines)
        + "\nส่วนใหญ่เกิดจาก start.py ที่ยังรันค้างอยู่ในอีกหน้าต่างหนึ่ง "
        "ให้ไปที่หน้าต่างนั้นแล้วกด Ctrl+C หรือปิดหน้าต่างนั้น จากนั้นรันคำสั่งนี้อีกครั้ง"
    )


# ---------------------------------------------------------------- prepare (runs to completion)


def run_step(command, cwd, failure_message):
    if subprocess.run([str(part) for part in command], cwd=cwd).returncode != 0:
        raise Stop(failure_message)


def prepare_python():
    heading("เตรียม Backend Python")
    if not venv_python().exists():
        say("สร้าง venv (ทำครั้งแรกครั้งเดียว)")
        run_step(
            [sys.executable, "-m", "venv", "venv"],
            PYTHON_DIR,
            "สร้าง venv ไม่สำเร็จ ดูข้อความ error ด้านบน",
        )
    say("ตรวจและติดตั้ง package ของ Python")
    run_step(
        [venv_python(), "-m", "pip", "install", "--quiet", "--disable-pip-version-check",
         "-r", "requirements.txt"],
        PYTHON_DIR,
        "ติดตั้ง package ของ Python ไม่สำเร็จ ดูข้อความ error ด้านบน "
        "(การรันครั้งแรกต้องต่ออินเทอร์เน็ต)",
    )


def prepare_frontend():
    heading("เตรียม Frontend")
    node = find_node()
    if (FRONTEND_DIR / "node_modules" / "vite" / "bin" / "vite.js").exists():
        say("package ของ frontend ติดตั้งไว้แล้ว")
    else:
        say("ติดตั้ง package ของ frontend (ครั้งแรกใช้เวลาสักครู่)")
        run_step(
            [shutil.which("npm"), "install"],
            FRONTEND_DIR,
            "npm install ไม่สำเร็จ ดูข้อความ error ด้านบน (การรันครั้งแรกต้องต่ออินเทอร์เน็ต)",
        )
    return node


def prepare_rust(cargo):
    heading("เตรียม Backend Rust")
    say("build โค้ด Rust (ครั้งแรกใช้เวลาหลายนาที ครั้งถัดไปจะเร็ว)")
    run_step(
        [cargo, "build"],
        RUST_DIR,
        f"build Backend Rust ไม่สำเร็จ ดูข้อความ error ด้านบน และดูวิธีแก้ใน {RUST_GUIDE}",
    )


# ---------------------------------------------------------------- run


def start(command, cwd):
    options = {}
    if not IS_WINDOWS:
        # Own process group, so stop_all can signal a service together with its children.
        options["start_new_session"] = True
    # A pipe that is never written to: the services must not read the terminal. Vite
    # closes when its stdin ends, and this pipe only ends when the launcher itself exits.
    return subprocess.Popen([str(part) for part in command], cwd=cwd, stdin=subprocess.PIPE, **options)


def _kill_tree(process, force):
    if IS_WINDOWS:
        if process.poll() is None:
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        return
    try:
        if force:
            os.killpg(process.pid, signal.SIGKILL)
        elif process.poll() is None:
            # Only the service itself: it closes its own children in order. Signalling
            # the whole group at once makes Vite log errors about its helper vanishing.
            process.terminate()
    except (ProcessLookupError, PermissionError):
        pass


def _wait_all(processes, seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if all(process.poll() is not None for process in processes):
            return
        time.sleep(0.1)


def stop_all(processes, ctrl_c):
    """Stop every service and whatever it started.

    On Windows a Ctrl+C already reached the services (they share this console), so
    give them a moment to exit by themselves; anything left is killed as a tree.
    On macOS/Linux ask each service to stop, then kill its whole process group.
    """
    processes = list(processes)
    try:
        if IS_WINDOWS:
            if ctrl_c:
                _wait_all(processes, SHUTDOWN_GRACE_SECONDS)
        else:
            for process in processes:
                _kill_tree(process, force=False)
            _wait_all(processes, SHUTDOWN_GRACE_SECONDS)
    except KeyboardInterrupt:
        pass  # a second Ctrl+C: stop waiting and kill now
    for process in processes:
        _kill_tree(process, force=True)
    for process in processes:
        try:
            process.wait(timeout=SHUTDOWN_GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            pass


def run_services(requested):
    explicit = bool(requested)
    selected = [name for name in SERVICES if name in requested] if explicit else list(SERVICES)

    cargo = None
    if "rust" in selected:
        cargo = find_cargo()
        if cargo is None:
            if explicit:
                raise Stop(f"ไม่พบ cargo ในเครื่อง ดูวิธีติดตั้ง Rust ใน {RUST_GUIDE}")
            selected.remove("rust")
            say(f"ไม่พบ Rust ในเครื่อง จึงข้าม Backend Rust (ไม่บังคับ ถ้าสนใจดู {RUST_GUIDE})")

    check_ports_free(selected)

    commands = {}
    if "frontend" in selected:
        node = prepare_frontend()
        vite = FRONTEND_DIR / "node_modules" / "vite" / "bin" / "vite.js"
        # Vite is started with node directly: going through npm on Windows runs a .cmd
        # file, which stops to ask "Terminate batch job (Y/N)?" on Ctrl+C.
        commands["frontend"] = ([node, vite, "--host", HOST, "--port", PORTS["frontend"], "--strictPort"], FRONTEND_DIR)
    if "python" in selected:
        prepare_python()
        commands["python"] = (
            [venv_python(), "-m", "uvicorn", "app.main:app", "--host", HOST,
             "--port", PORTS["python"], "--reload", "--reload-dir", "app"],
            PYTHON_DIR,
        )
    if "rust" in selected:
        try:
            prepare_rust(cargo)
        except Stop as problem:
            if explicit:
                raise
            say(str(problem))
            say("ข้าม Backend Rust แล้วรันส่วนที่เหลือต่อ")
            selected.remove("rust")
        else:
            # Must run from backend-rust: the data paths in storage_service.rs are relative.
            commands["rust"] = ([cargo, "run"], RUST_DIR)

    heading("เริ่มรัน " + ", ".join(LABELS[name] for name in selected))
    processes = {}
    ctrl_c = False
    try:
        for name in selected:
            command, cwd = commands[name]
            processes[name] = start(command, cwd)

        ready = False
        while True:
            for name, process in processes.items():
                code = process.poll()
                if code is not None:
                    raise Stop(f"{LABELS[name]} หยุดทำงานเอง (exit code {code}) ดูข้อความ error ด้านบน")
            if not ready and all(port_in_use(PORTS[name], (HOST,)) for name in processes):
                ready = True
                _print_ready(selected)
            time.sleep(0.5)
    except KeyboardInterrupt:
        ctrl_c = True
    finally:
        say()
        say("กำลังปิดทุก service ...")
        stop_all(processes.values(), ctrl_c)

    still_open = [name for name in processes if port_in_use(PORTS[name], (HOST,))]
    if still_open:
        ports = ", ".join(str(PORTS[name]) for name in still_open)
        say(f"คำเตือน: พอร์ต {ports} ยังถูกใช้อยู่ อาจมีโปรแกรมค้าง ให้ปิดหน้าต่าง terminal นี้แล้วเปิดใหม่")
        return 1
    say("ปิดครบแล้ว")
    return 0


def _print_ready(selected):
    say()
    say("=" * 60)
    say("พร้อมใช้งานแล้ว")
    if "frontend" in selected:
        say(f"  เปิดแผนที่ในเบราว์เซอร์:  http://localhost:{PORTS['frontend']}")
    if "python" in selected:
        say(f"  Backend Python:          http://localhost:{PORTS['python']}/api/health")
    if "rust" in selected:
        say(f"  Backend Rust:            http://localhost:{PORTS['rust']}/api/health")
    say("กด Ctrl+C ในหน้าต่างนี้เมื่อต้องการปิด")
    say("=" * 60)
    say()


# ---------------------------------------------------------------- test


def run_tests():
    say("หมายเหตุ: test เขียนและลบข้อมูลใน user_drawings.geojson จริง")
    prepare_python()
    heading("test ของ Backend Python")
    failed = subprocess.run([str(venv_python()), "-m", "pytest"], cwd=PYTHON_DIR).returncode != 0

    cargo = find_cargo()
    if cargo is None:
        say()
        say(f"ไม่พบ Rust ในเครื่อง จึงข้าม test ของ Backend Rust (ดู {RUST_GUIDE})")
    else:
        heading("test ของ Backend Rust")
        failed = subprocess.run([cargo, "test"], cwd=RUST_DIR).returncode != 0 or failed

    say()
    say("มี test ที่ไม่ผ่าน ดูรายละเอียดด้านบน" if failed else "test ผ่านทั้งหมด")
    return 1 if failed else 0


# ---------------------------------------------------------------- entry point


def _interrupt(signum, frame):
    raise KeyboardInterrupt


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    if sys.version_info < (3, 10):
        say(f"ต้องใช้ Python 3.10 ขึ้นไป (เครื่องนี้เป็น {sys.version.split()[0]})")
        return 2

    arguments = [argument.lower() for argument in argv[1:]]
    if any(argument in ("-h", "--help", "help") for argument in arguments):
        say(__doc__.split("For maintainers:")[0].rstrip())
        return 0

    # Closing the terminal or a plain `kill` must stop the services too, not orphan them.
    for name in ("SIGTERM", "SIGHUP", "SIGBREAK"):
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), _interrupt)

    try:
        if arguments == ["test"]:
            return run_tests()
        unknown = [argument for argument in arguments if argument not in SERVICES]
        if unknown:
            say(f"ไม่รู้จักคำว่า {' '.join(unknown)}")
            say(__doc__.split("For maintainers:")[0].rstrip())
            return 2
        return run_services(arguments)
    except Stop as problem:
        say()
        say(str(problem))
        return 1
    except KeyboardInterrupt:
        say()
        say("ยกเลิกแล้ว")
        return 130


if __name__ == "__main__":
    sys.exit(main(sys.argv))
