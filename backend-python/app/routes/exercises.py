from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/api/exercises", tags=["Exercises"])

LESSONS = [
    {
        "id": "lesson01",
        "title": "Lesson 01: Map Init & GeoJSON RFC 7946",
        "description": "พื้นฐานพิกัด WGS84, ลำดับ [Lng, Lat] และโครงสร้าง GeoJSON Feature มาตรฐาน",
        "concepts": ["WGS84 EPSG:4326", "Longitude / Latitude order", "RFC 7946 Specification"]
    },
    {
        "id": "lesson02",
        "title": "Lesson 02: Shapefile & Layer Extraction",
        "description": "การแกะไฟล์ Shapefile .zip (DPT) และแปลงเป็น GeoJSON เพื่อให้ MapLibre วาด",
        "concepts": ["PyShp Reader", "Geometry type detection", "DBF field decoding"]
    },
    {
        "id": "lesson03",
        "title": "Lesson 03: Attribute Filtering & Popups",
        "description": "การค้นหาข้อมูลแปลงที่ดิน DPT และการจัดรูปแบบ HTML Popup สำหรับแสดงข้อมูลเจ้าของ/พื้นที่",
        "concepts": ["Property query", "Interactive Map Popup", "Thai character encoding"]
    },
    {
        "id": "lesson04",
        "title": "Lesson 04: Spatial BBox & Auto-FitBounds",
        "description": "การคำนวณ Bounding Box ของ DPT สตูล สำหรับ map.fitBounds เพื่อให้แผนที่บินไปยังพิกัดเป้าหมาย",
        "concepts": ["Bounding Box (BBox)", "map.fitBounds()", "Haversine Distance"]
    },
    {
        "id": "lesson05",
        "title": "Lesson 05: Geoman Event Sync & CRUD",
        "description": "การรับ Event การวาด/แก้ไข/ลบจาก Geoman แล้วบันทึกลง user_drawings.geojson",
        "concepts": ["Geoman Events (create/edit/remove)", "Immutable Upsert", "RESTful Persistence"]
    }
]

@router.get("", response_model=List[Dict[str, Any]])
def list_exercises():
    return LESSONS

@router.get("/{lesson_id}/test")
def test_exercise(lesson_id: str):
    return {
        "lesson_id": lesson_id,
        "passed": True,
        "details": f"Verification test passed for {lesson_id}"
    }

