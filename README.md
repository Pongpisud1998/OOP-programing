# MapLibre GIS Learning Studio & Dual-Backend API Hub

โปรเจกต์เว็บแอปพลิเคชันและแบบฝึกหัดพัฒนาแผนที่แบบ Interactive Full-Stack สำหรับศึกษาการใช้งาน **MapLibre GL JS**, แถบเครื่องมือวาด/แก้ไข/ลบด้วย **Geoman (`@geoman-io/maplibre-geoman-free`)**, และการเชื่อมต่อ **RESTful API** สองภาษา:
- **Rust (Axum - Port 8080)**: เสิร์ฟข้อมูลผังภาษีและที่ดินจริง **LTAX GeoJSON (ขอนแก่น)**
- **Python (FastAPI - Port 8000)**: เสิร์ฟข้อมูลผังเมืองจริง **DPT Shapefile .zip (สตูล)**
- **React + TypeScript (Vite - Port 5173)**: หน้าบ้านเว็บแผนที่ มีตัวสลับ Backend, Auto-FitBounds, Layer Manager, Popups และ Geoman Toolbar

---

## 1. จุดเด่นของโปรเจกต์ (Key Features)

1. **Dual-Backend Switcher**: สลับระหว่าง Rust (Axum) กับ Python (FastAPI) ได้ทันทีจากแถบเมนูด้านบน
2. **Auto-FitBounds Camera**: เมื่อสลับ Backend แผนที่จะบิน (FlyTo) ไปยัง Bounding Box ของข้อมูลนั้นอัตโนมัติ (ขอนแก่น vs สตูล)
3. **Real-world GIS Data**:
   - **LTAX (Rust)**: ขอบเขตเทศบาล, โซนภาษี, บล็อกภาษี, แปลงที่ดิน (Parcel กว่า 3,600 แปลง), อาคารสิ่งปลูกสร้าง (Building กว่า 1,500 อาคาร)
   - **DPT (FastAPI)**: ขอบเขตผังเมืองสตูล, แปลงที่ดินผังเมือง (พร้อมชื่อเจ้าของภาษาไทย), ที่สาธารณประโยชน์, พื้นที่สาธารณูปโภค
4. **Geoman Drawing & Vertex Editing**:
   - วาด Marker (จุด), Line (เส้น), Polygon (โพลิกอน), Rectangle (สี่เหลี่ยม)
   - โหมด Edit Vertices (ดึง/ขยับจุดยอดของรูปทรง), Drag Mode, และ Trash (ลบ)
   - ซิงค์การวาด/แก้ไข/ลบ เข้าสู่ `user_drawings.geojson` ของ Backend ที่เลือกไว้แบบ Real-time พร้อมปุ่ม Reset คืนค่าเริ่มต้น
5. **Interactive Popups**: คลิกที่รูปทรงบนแผนที่เพื่อดูข้อมูล Attribute ภาษาไทย (ชื่อเจ้าของ, รหัสแปลง, ประเภทผังเมือง, ขนาดพื้นที่)
6. **5 Step-by-Step Lessons**: มีแถบหลักสูตร 5 บทเรียนพร้อมตัวอย่างโค้ดเปรียบเทียบ 3 ภาษา (React, Python, Rust) และปุ่ม Run Test ตรวจผลลัพธ์

---

## 2. โครงสร้างโปรเจกต์ (Project Structure)

```text
OOP-programing/
├── data/
│   ├── ltax/
│   │   ├── geojson/              # ข้อมูล LTAX ขอนแก่น (boundary, zone, block, parcel, building)
│   │   └── user_drawings.geojson # ข้อมูลที่ผู้ใช้วาดผ่าน Geoman ในฝั่ง Rust
│   └── dpt/
│       ├── shapefile/            # ข้อมูล DPT สตูล (.zip archives: boundary, be_parcel, be_public, af_public)
│       └── user_drawings.geojson # ข้อมูลที่ผู้ใช้วาดผ่าน Geoman ในฝั่ง FastAPI
│
├── frontend/                     # React + TypeScript + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/
│   │   │   ├── MapView.tsx       # MapLibre Canvas & Geoman Integration
│   │   │   ├── LayerManager.tsx  # แผงจัดการเปิด/ปิดเลเยอร์, Opacity, สี
│   │   │   ├── Navbar.tsx        # แถบเมนู, สลับ Backend, สถานะเซิร์ฟเวอร์
│   │   │   └── LearningSidebar.tsx # หลักสูตร 5 บทเรียน, Code Viewer, Run Test
│   │   ├── services/api.ts       # API Client รองรับทั้ง Rust (:8080) และ FastAPI (:8000)
│   │   └── App.tsx               # Main Layout
│   └── package.json
│
├── backend-python/               # Python FastAPI REST API
│   ├── app/
│   │   ├── main.py               # FastAPI entrypoint (Port 8000)
│   │   ├── services/shapefile_service.py # Auto-unzip & PyShp GeoJSON parser
│   │   └── routes/               # layers.py, features.py, exercises.py
│   ├── tests/                    # Pytest test suite
│   ├── requirements.txt
│   └── run.sh
│
├── backend-rust/                 # Rust Axum REST API
│   ├── src/
│   │   ├── main.rs               # Axum entrypoint (Port 8080)
│   │   ├── services/storage_service.rs # High-speed LTAX GeoJSON reader & CRUD
│   │   └── routes/               # layers.rs, features.rs, exercises.rs
│   ├── Cargo.toml
│   └── run.sh
│
├── start.sh                      # สคริปต์คำสั่งเดียว รันครบทั้ง 3 services
├── .gitignore                    # กรองไฟล์ cache, target, venv, os files
└── package.json                  # Root npm scripts
```

---

## 3. วิธีการติดตั้งและรันโปรเจกต์ (Quick Start)

### วิธีที่ 1: รันคำสั่งเดียวเปิดครบ 3 Services (แนะนำ)
เปิด Terminal ที่ root directory แล้วรัน:
```bash
./start.sh
```
สคริปต์จะเริ่มทำงานพร้อมกัน:
- 🐍 Python FastAPI: [http://localhost:8000](http://localhost:8000)
- 🦀 Rust Axum: [http://localhost:8080](http://localhost:8080)
- ⚛️ React Frontend: [http://localhost:5173](http://localhost:5173)

---

### วิธีที่ 2: รันแยกทีละ Service สำหรับการเรียนรู้

#### 1. Backend Python (FastAPI)
```bash
cd backend-python
./run.sh
# หรือรันผ่าน venv
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
ทดสอบ Unit Test:
```bash
cd backend-python
PYTHONPATH=. venv/bin/pytest
```

#### 2. Backend Rust (Axum)
```bash
cd backend-rust
cargo run
```
ทดสอบ Unit Test:
```bash
cd backend-rust
cargo test
```

#### 3. Frontend (React TypeScript)
```bash
cd frontend
npm install
npm run dev
```

---

## 4. REST API Documentation (ตรงกันทั้ง Python & Rust)

| Method | Endpoint | รายละเอียด |
|---|---|---|
| `GET` | `/api/health` | ตรวจสอบสถานะการเชื่อมต่อ และระบุชื่อ Backend/Dataset |
| `GET` | `/api/layers` | ดึงรายชื่อเลเยอร์ทั้งหมด พร้อม metadata, จำนวนฟีเจอร์ และ BBox |
| `GET` | `/api/layers/{layer_id}` | ดึงข้อมูล GeoJSON `FeatureCollection` สำหรับวาดบนแผนที่ |
| `POST` | `/api/features` | บันทึก Feature ที่วาดใหม่จาก Geoman ลง `user_drawings.geojson` |
| `PUT` | `/api/features/{id}` | อัปเดตพิกัด/ข้อมูลของ Feature ที่ถูกแก้ไข |
| `DELETE` | `/api/features/{id}` | ลบ Feature ออกจากระบบ |
| `POST` | `/api/reset` | รีเซ็ตชั้นข้อมูลที่วาดให้กลับเป็นค่าเริ่มต้น |
| `GET` | `/api/exercises` | ดูรายการบทเรียน 5 สเต็ป |
| `GET` | `/api/exercises/{lesson_id}/test` | รันแบบทดสอบประจำบทเรียน |

