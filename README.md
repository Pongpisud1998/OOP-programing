# คอร์สพื้นฐานการเขียนโปรแกรม และ MapLibre GIS Learning Studio

โปรเจกต์นี้มีสองส่วน

1. **คอร์สพื้นฐานการเขียนโปรแกรมด้วย Python** สำหรับคนที่ไม่เคยเขียนโปรแกรมมาก่อน อยู่ในโฟลเดอร์ [course/](course/)
2. **เว็บแอปแผนที่** ที่แสดงข้อมูลแปลงที่ดินจริง เป็นปลายทางของคอร์ส และเป็นเนื้อหาภาคต่อด้าน GIS

---

## เริ่มตรงนี้ (สำหรับน้องฝึกงาน)

ยังไม่ต้องอ่านส่วนอื่นของหน้านี้ และยังไม่ต้องรันเว็บแอปแผนที่

1. เปิด [course/README.md](course/README.md) อ่านวิธีเรียนและกติกา
2. เริ่มบทแรกที่ [course/lesson00_setup/README.md](course/lesson00_setup/README.md) ซึ่งจะพาติดตั้งเครื่องมือทั้งหมดทีละขั้น

---

## สำหรับผู้ดูแลโปรเจกต์

เนื้อหาตั้งแต่ตรงนี้ลงไปเป็นรายละเอียดทางเทคนิคของเว็บแอปแผนที่

### ภาพรวม

เว็บแอปแผนที่แบบ full-stack สำหรับศึกษา **MapLibre GL JS** เครื่องมือวาดและแก้ไขรูปทรงด้วย **Geoman** (`@geoman-io/maplibre-geoman-free`) และการเชื่อมต่อ **REST API**

| ส่วน | เทคโนโลยี | พอร์ต | ข้อมูล |
|---|---|---|---|
| Backend หลัก | Python (FastAPI) | 8000 | DPT Shapefile .zip (สตูล) |
| Backend เสริม | Rust (Axum) | 8080 | LTAX GeoJSON (ขอนแก่น) |
| Frontend | React + TypeScript (Vite) | 5173 | |

Frontend เริ่มต้นที่ backend Python ส่วน Rust เป็นตัวเลือกเสริม ไม่ต้องติดตั้งก็ใช้งานแอปได้

### ความสามารถ

1. **สลับ backend** ระหว่าง Python กับ Rust จากแถบเมนูด้านบน แผนที่จะย้ายมุมมองไปยังขอบเขตของข้อมูลชุดนั้น (สตูลหรือขอนแก่น)
2. **ข้อมูล GIS จริง**
   - DPT (Python): ขอบเขตผังเมือง แปลงที่ดิน 40 แปลงพร้อมชื่อเจ้าของ ที่สาธารณประโยชน์ พื้นที่สาธารณูปโภค
   - LTAX (Rust): ขอบเขตเทศบาล โซนภาษี บล็อกภาษี แปลงที่ดินกว่า 3,600 แปลง อาคารกว่า 1,500 หลัง
3. **วาดและแก้ไขด้วย Geoman**: จุด เส้น โพลิกอน สี่เหลี่ยม แก้จุดยอด ลาก และลบ โดยบันทึกลง `user_drawings.geojson` ของ backend ที่เลือกอยู่ มีปุ่ม Reset คืนค่าเริ่มต้น
4. **Popup**: คลิกรูปทรงบนแผนที่เพื่อดูข้อมูล attribute
5. **แถบเนื้อหา GIS 5 หัวข้อ** พร้อมตัวอย่างโค้ดเปรียบเทียบ 3 ภาษา ใช้เป็นเอกสารอ่านประกอบภาคต่อ ไม่มีการตรวจอัตโนมัติ

### โครงสร้างโปรเจกต์

```text
OOP-programing/
├── course/                       # คอร์สพื้นฐาน Python
│   ├── README.md                 # วิธีเรียน กติกา รายการบท
│   ├── check.py                  # ตัวตรวจแบบฝึกหัด: python check.py <เลขบท>
│   ├── checklib.py               # ไลบรารีของตัวตรวจ (standard library ล้วน)
│   └── lessonNN_*/               # แต่ละบท: README.md, exercise.py, hints.md, checks.py
│
├── data/
│   ├── dpt/
│   │   ├── shapefile/            # ข้อมูล DPT สตูล (.zip) และ Satul_CSV_new.csv
│   │   └── user_drawings.geojson # รูปทรงที่ผู้ใช้วาด ฝั่ง Python
│   └── ltax/
│       ├── geojson/              # ข้อมูล LTAX ขอนแก่น
│       └── user_drawings.geojson # รูปทรงที่ผู้ใช้วาด ฝั่ง Rust
│
├── backend-python/               # Python FastAPI (พอร์ต 8000)
│   ├── app/
│   │   ├── main.py
│   │   ├── services/shapefile_service.py
│   │   └── routes/               # layers.py, features.py
│   ├── tests/
│   ├── requirements.txt
│   └── run.sh
│
├── backend-rust/                 # Rust Axum (พอร์ต 8080)
│   ├── src/
│   │   ├── main.rs
│   │   ├── services/storage_service.rs
│   │   └── routes/               # layers.rs, features.rs
│   ├── Cargo.toml
│   └── run.sh
│
├── frontend/                     # React + TypeScript + Vite + Tailwind CSS
│   └── src/
│       ├── components/           # MapView, LayerManager, Navbar, LearningSidebar
│       ├── services/api.ts
│       └── App.tsx
│
└── start.sh                      # รันทุก service ด้วยคำสั่งเดียว (macOS / Linux)
```

### วิธีรันเว็บแอปแผนที่

**รันทุก service ด้วยคำสั่งเดียว (macOS / Linux)**

```bash
./start.sh
```

สคริปต์จะสร้าง venv และติดตั้ง package ของ Python ให้เอง และข้าม backend Rust ถ้าเครื่องไม่มี `cargo`

- Python FastAPI: http://localhost:8000
- Rust Axum: http://localhost:8080
- Frontend: http://localhost:5173

**รันแยกทีละ service**

```bash
# Backend Python
cd backend-python
./run.sh

# Backend Rust (ไม่บังคับ)
cd backend-rust
./run.sh

# Frontend
cd frontend
npm install
npm run dev
```

**รัน test**

```bash
cd backend-python && venv/bin/pytest
cd backend-rust && cargo test
```

test ของทั้งสอง backend เขียนและลบข้อมูลใน `user_drawings.geojson` จริง

**ตรวจว่าแบบฝึกหัดของคอร์สยังใช้งานได้**

```bash
cd course
python3 check.py 1                          # ตรวจไฟล์ exercise.py ของบท 1
python3 check.py 1 path/to/solution.py      # ตรวจไฟล์อื่นด้วยเกณฑ์ของบท 1 (ใช้กับเฉลย)
```

เฉลยและคู่มือผู้สอนเก็บแยกไว้นอก repo นี้

### REST API (เหมือนกันทั้ง Python และ Rust)

| Method | Endpoint | รายละเอียด |
|---|---|---|
| `GET` | `/api/health` | สถานะของ backend และชื่อชุดข้อมูล |
| `GET` | `/api/layers` | รายชื่อเลเยอร์ พร้อม metadata จำนวน feature และ bbox |
| `GET` | `/api/layers/{layer_id}` | GeoJSON `FeatureCollection` ของเลเยอร์ |
| `POST` | `/api/features` | บันทึก feature ที่วาดใหม่ลง `user_drawings.geojson` |
| `PUT` | `/api/features/{id}` | อัปเดต feature ที่ถูกแก้ไข |
| `DELETE` | `/api/features/{id}` | ลบ feature |
| `POST` | `/api/reset` | ล้างรูปทรงที่วาดทั้งหมด (`/api/features/reset` ใช้ได้เช่นกัน) |
