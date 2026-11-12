"""เครื่องมือตรวจแบบฝึกหัดของคอร์ส

น้องฝึกงานไม่ต้องแก้หรืออ่านไฟล์นี้ ใช้ผ่านคำสั่ง  python check.py <เลขบท>  ก็พอ

For maintainers: each lesson folder has a checks.py that builds a Lesson and
registers checks with @lesson.check(...). A check receives a Tester, which runs
the intern's exercise.py and can re-run it with different starting values
(see Tester.run) so that typing the final answer in by hand does not pass.
Uses the standard library only, so lessons 0-8 need nothing installed.
"""

import ast
import contextlib
import io
import sys
import traceback
from pathlib import Path

COURSE_DIR = Path(__file__).resolve().parent

ERROR_HELP = {
    "SyntaxError": "เขียนผิดรูปแบบของภาษา มักเกิดจากลืมปิดเครื่องหมายคำพูด ลืมปิดวงเล็บ "
    "หรือลืมเครื่องหมาย : ท้ายบรรทัด if / else ให้ดูทั้งบรรทัดนี้และบรรทัดก่อนหน้า",
    "IndentationError": "ย่อหน้าไม่ถูกต้อง บรรทัดทั่วไปต้องชิดซ้ายสุด "
    "ส่วนบรรทัดที่อยู่ใต้ if / else ต้องเว้นวรรคด้านหน้า 4 ช่องเท่ากันทุกบรรทัด",
    "NameError": "Python ไม่รู้จักชื่อนี้ ตรวจตัวสะกดและตัวพิมพ์เล็ก-ใหญ่ "
    "ถ้าตั้งใจให้เป็นข้อความต้องอยู่ในเครื่องหมายคำพูด "
    "ถ้าเป็นตัวแปรต้องถูกสร้างก่อนบรรทัดที่นำมาใช้",
    "TypeError": "นำค่าคนละชนิดมาใช้ร่วมกันแบบนี้ไม่ได้ เช่น เอาข้อความไปบวกกับตัวเลข",
    "ZeroDivisionError": "หารด้วยศูนย์ไม่ได้",
    "ValueError": "ค่าที่ส่งให้คำสั่งนี้ไม่อยู่ในรูปแบบที่คำสั่งรับได้",
    "EOFError": "โปรแกรมรอรับข้อมูลจากแป้นพิมพ์ด้วย input() ซึ่งแบบฝึกหัดนี้ไม่ต้องใช้",
}


class CheckFailed(Exception):
    """Raised by a check with a Thai message explaining what is still wrong."""


class StudentError:
    """An error raised by the intern's own code, located in their file."""

    def __init__(self, type_name, message, line_no, line_text):
        self.type_name = type_name
        self.message = message
        self.line_no = line_no
        self.line_text = line_text

    def short(self):
        where = f" (บรรทัด {self.line_no})" if self.line_no else ""
        return f"{self.type_name}: {self.message}{where}"


class RunResult:
    def __init__(self, variables, output, error):
        self.variables = variables
        self.output = output
        self.error = error

    def lines(self):
        return [line.rstrip() for line in self.output.splitlines()]


def show(value):
    """Format a value the way the intern would type it."""
    if isinstance(value, str):
        return f'"{value}"'
    return repr(value)


def describe_given(given):
    if not given:
        return ""
    parts = [f"{name} = {show(value)}" for name, value in given.items()]
    return "เมื่อ " + " และ ".join(parts) + " "


def _override_starting_values(tree, given):
    """Replace top-level `name = <value>` lines with the values in `given`."""
    remaining = dict(given)
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id in remaining:
            node.value = ast.copy_location(ast.Constant(remaining.pop(target.id)), node.value)
    if remaining:
        names = ", ".join(remaining)
        raise CheckFailed(
            f"ไม่พบบรรทัดค่าตั้งต้นของ {names} ที่โจทย์ให้มา "
            "บรรทัดเหล่านั้นต้องอยู่เหมือนเดิม ถ้าเผลอลบหรือแก้ไป ให้พิมพ์กลับตามโจทย์"
        )
    ast.fix_missing_locations(tree)


def run_exercise(path, given=None):
    """Run the intern's file and collect its variables, printed output and any error."""
    source = Path(path).read_text(encoding="utf-8")
    source_lines = source.splitlines()
    filename = str(path)

    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as exc:
        line_text = (exc.text or "").strip()
        return RunResult({}, "", StudentError(type(exc).__name__, exc.msg, exc.lineno, line_text))

    if given:
        _override_starting_values(tree, given)

    code = compile(tree, filename, "exec")
    env = {"__name__": "__main__", "__file__": filename}
    output = io.StringIO()
    error = None
    real_stdin = sys.stdin
    sys.stdin = io.StringIO("")
    try:
        with contextlib.redirect_stdout(output):
            exec(code, env)
    except (Exception, SystemExit) as exc:
        line_no = None
        for frame in traceback.extract_tb(exc.__traceback__):
            if frame.filename == filename:
                line_no = frame.lineno
        line_text = ""
        if line_no and line_no <= len(source_lines):
            line_text = source_lines[line_no - 1].strip()
        error = StudentError(type(exc).__name__, str(exc), line_no, line_text)
    finally:
        sys.stdin = real_stdin

    variables = {name: value for name, value in env.items() if not name.startswith("__")}
    return RunResult(variables, output.getvalue(), error)


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _mismatch(actual, expected):
    """Return None when the values match, otherwise a Thai phrase describing `actual`."""
    if isinstance(expected, bool):
        if isinstance(actual, bool):
            return None if actual == expected else f"ได้ {show(actual)}"
        return f"ได้ {show(actual)} ซึ่งไม่ใช่ค่า True หรือ False"
    if _is_number(expected):
        if _is_number(actual):
            return None if abs(actual - expected) < 1e-6 else f"ได้ {show(actual)}"
        if isinstance(actual, str):
            return f"ได้ข้อความ {show(actual)} โจทย์ต้องการตัวเลข (ไม่มีเครื่องหมายคำพูด)"
        return f"ได้ {show(actual)} ซึ่งไม่ใช่ตัวเลข"
    if isinstance(expected, str):
        if not isinstance(actual, str):
            return f"ได้ {show(actual)} ซึ่งไม่ใช่ข้อความ"
        if actual == expected:
            return None
        if "".join(actual.split()) == "".join(expected.split()):
            return f"ได้ {show(actual)} ซึ่งต่างกันที่ช่องว่าง ให้เทียบทีละตัวอักษร"
        return f"ได้ {show(actual)}"
    return None if actual == expected else f"ได้ {show(actual)}"


class Tester:
    """Gives checks access to one exercise file."""

    def __init__(self, path):
        self.path = Path(path)
        self._runs = {}
        self._tips_shown = set()

    def _first_time(self, tip):
        """True only the first time a tip is asked for, so repeated advice prints once."""
        if tip in self._tips_shown:
            return False
        self._tips_shown.add(tip)
        return True

    def run(self, given=None):
        """Run the exercise, optionally replacing starting values, e.g. given={"rai": 5}."""
        key = tuple(sorted((given or {}).items(), key=lambda item: item[0]))
        if key not in self._runs:
            self._runs[key] = run_exercise(self.path, given)
        return self._runs[key]

    def var(self, name, given=None):
        result = self.run(given)
        if name in result.variables:
            return result.variables[name]
        prefix = describe_given(given)
        if result.error and given:
            raise CheckFailed(f"{prefix}โปรแกรมหยุดทำงาน: {result.error.short()}")
        if result.error:
            raise CheckFailed(f"ยังตรวจไม่ได้ เพราะโปรแกรมหยุดทำงานก่อนจะสร้างตัวแปร {name}")
        if given:
            raise CheckFailed(
                f"{prefix}โค้ดไม่ได้สร้างตัวแปร {name} "
                "(ถ้าใช้ if อยู่ ดูว่ามีทางเลือกรองรับกรณีนี้หรือยัง)"
            )
        message = f"ยังไม่พบตัวแปรชื่อ {name}"
        if self._first_time("missing-variable"):
            message += " (ชื่อต้องสะกดตรงกับโจทย์ทุกตัวอักษร รวมถึงตัวพิมพ์เล็ก-ใหญ่)"
        raise CheckFailed(message)

    def var_equals(self, name, expected, given=None):
        actual = self.var(name, given)
        problem = _mismatch(actual, expected)
        if problem is None:
            return
        message = f"{describe_given(given)}ตัวแปร {name} ควรเป็น {show(expected)} แต่{problem}"
        if given:
            base = self.run().variables.get(name)
            if type(base) is type(actual) and base == actual:
                message += (
                    "\nค่านี้เท่ากับตอนที่ยังไม่เปลี่ยนค่าตั้งต้น "
                    "แปลว่าโค้ดอาจพิมพ์คำตอบลงไปตรง ๆ แทนที่จะคำนวณจากตัวแปร"
                )
        raise CheckFailed(message)

    def _output_summary(self):
        if not self._first_time("output-summary"):
            return ""
        lines = [line for line in self.run().lines() if line]
        if not lines:
            return "ตอนนี้โปรแกรมยังไม่แสดงอะไรออกมาเลย"
        shown = "\n".join("    " + line for line in lines[:8])
        more = "\n    ..." if len(lines) > 8 else ""
        return f"สิ่งที่โปรแกรมแสดงออกมาตอนนี้:\n{shown}{more}"

    def output_has_line(self, text):
        if text in self.run().lines():
            return
        raise CheckFailed(f"ยังไม่เจอบรรทัด  {text}  ในผลลัพธ์\n{self._output_summary()}".rstrip())

    def output_has_line_starting(self, prefix, what_follows):
        for line in self.run().lines():
            if line.startswith(prefix) and line[len(prefix):].strip():
                return
        raise CheckFailed(
            f"ยังไม่เจอบรรทัดที่ขึ้นต้นด้วย  {prefix}  แล้วตามด้วย{what_follows}\n{self._output_summary()}".rstrip()
        )

    def output_lacks(self, text):
        if text in self.run().output:
            raise CheckFailed(f"ผลลัพธ์ยังมีข้อความ  {text}  อยู่ ซึ่งโจทย์ไม่ต้องการให้แสดง")


class Lesson:
    def __init__(self, number, title):
        self.number = number
        self.title = title
        self.checks = []

    def check(self, title, challenge=False):
        def register(func):
            self.checks.append((title, challenge, func))
            return func

        return register


def find_lesson_dir(number):
    matches = sorted(COURSE_DIR.glob(f"lesson{number:02d}_*"))
    return matches[0] if matches else None


def available_lessons():
    numbers = []
    for folder in sorted(COURSE_DIR.glob("lesson[0-9][0-9]_*")):
        if (folder / "checks.py").exists():
            numbers.append(int(folder.name[6:8]))
    return numbers


def load_lesson(lesson_dir):
    import importlib.util

    if str(COURSE_DIR) not in sys.path:
        sys.path.insert(0, str(COURSE_DIR))
    spec = importlib.util.spec_from_file_location(f"checks_{lesson_dir.name}", lesson_dir / "checks.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.lesson


def _indent(text, prefix="        "):
    return "\n".join(prefix + line for line in text.splitlines())


def _print_student_error(error):
    print()
    if error.type_name in ("SyntaxError", "IndentationError", "TabError"):
        print(f"Python อ่านไฟล์ไม่ได้ที่บรรทัด {error.line_no} โปรแกรมจึงยังไม่ได้เริ่มทำงานเลยสักบรรทัด")
    else:
        print(f"โปรแกรมหยุดทำงานที่บรรทัด {error.line_no}")
        print("โค้ดก่อนบรรทัดนี้ทำงานไปแล้ว ส่วนโค้ดหลังจากนี้ยังไม่ได้ทำงาน")
    if error.line_text:
        print(f"    {error.line_text}")
    print(f"{error.type_name}: {error.message}")
    help_text = ERROR_HELP.get(error.type_name) or ERROR_HELP.get(
        "SyntaxError" if error.type_name == "TabError" else ""
    )
    if help_text:
        print(f"แปลว่า: {help_text}")
    print()


def _usage():
    lessons = available_lessons()
    print("วิธีใช้:  python check.py <เลขบท>     เช่น  python check.py 1")
    if lessons:
        print("บทที่ตรวจได้ตอนนี้: " + ", ".join(str(n) for n in lessons))


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    if len(argv) < 2 or not argv[1].isdigit():
        _usage()
        return 2

    number = int(argv[1])
    lesson_dir = find_lesson_dir(number)
    if lesson_dir is None or not (lesson_dir / "checks.py").exists():
        print(f"ยังไม่มีบทที่ {number} ให้ตรวจ")
        _usage()
        return 2

    # Optional second argument: check a different file (used to verify the solutions).
    exercise_path = Path(argv[2]).resolve() if len(argv) > 2 else lesson_dir / "exercise.py"
    if not exercise_path.exists():
        print(f"ไม่พบไฟล์ {exercise_path}")
        return 2

    lesson = load_lesson(lesson_dir)
    tester = Tester(exercise_path)

    print(f"ตรวจบทที่ {lesson.number}: {lesson.title}")
    try:
        shown_path = exercise_path.relative_to(Path.cwd().resolve())
    except ValueError:
        shown_path = exercise_path
    print(f"ไฟล์: {shown_path}")

    base = tester.run()
    if base.error:
        _print_student_error(base.error)
        if not base.variables and not base.output:
            # Nothing ran at all (a syntax error): listing every check as failed is just noise.
            print("แก้จุดนี้ก่อน แล้วรันตัวตรวจอีกครั้ง")
            return 1
    else:
        print()

    counts = {False: [0, 0], True: [0, 0]}  # challenge? -> [passed, total]
    for title, challenge, func in lesson.checks:
        counts[challenge][1] += 1
        label = f"ท้าทาย {counts[challenge][1]}" if challenge else f"ข้อ {counts[challenge][1]}"
        try:
            func(tester)
        except CheckFailed as failure:
            print(f"  [ยังไม่ผ่าน] {label}  {title}")
            print(_indent(str(failure)))
        except Exception as exc:  # a bug in the checks themselves, not the intern's fault
            print(f"  [ตรวจไม่ได้] {label}  {title}")
            print(_indent(f"ตัวตรวจมีปัญหาเอง ไม่ใช่ความผิดของเรา แจ้งพี่เลี้ยงพร้อมข้อความนี้: {exc!r}"))
        else:
            counts[challenge][0] += 1
            print(f"  [ผ่าน]      {label}  {title}")

    passed, total = counts[False]
    print()
    print(f"ข้อบังคับ: ผ่าน {passed} จาก {total} ข้อ")
    if counts[True][1]:
        print(f"ข้อท้าทาย: ผ่าน {counts[True][0]} จาก {counts[True][1]} ข้อ (ไม่บังคับ)")

    if passed == total:
        print()
        print("ผ่านข้อบังคับครบแล้ว ขั้นต่อไป: commit แล้ว push งานขึ้น branch ของตัวเอง")
        print("และเตรียมอธิบายโค้ดแต่ละข้อให้พี่เลี้ยงฟังด้วยคำพูดของตัวเอง")
        return 0
    return 1
