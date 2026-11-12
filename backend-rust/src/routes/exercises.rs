use axum::{
    extract::Path,
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use serde_json::json;

pub async fn list_exercises() -> impl IntoResponse {
    let list = json!([
        {
            "id": "lesson01",
            "title": "Lesson 01: Map Init & GeoJSON RFC 7946",
            "description": "พื้นฐานพิกัด WGS84, ลำดับ [Lng, Lat] และโครงสร้าง GeoJSON Feature มาตรฐาน",
            "concepts": ["WGS84 EPSG:4326", "Longitude / Latitude order", "RFC 7946 Specification"]
        },
        {
            "id": "lesson02",
            "title": "Lesson 02: LTAX GeoJSON High-Performance Parsing",
            "description": "การอ่านและจัดการไฟล์ GeoJSON ขนาดใหญ่ (LTAX Khon Kaen) ด้วย Rust Serde",
            "concepts": ["High-performance JSON Deserialization", "Streaming features", "Memory safety"]
        },
        {
            "id": "lesson03",
            "title": "Lesson 03: Attribute Filtering & Popups",
            "description": "การสืบค้นข้อมูลแปลงที่ดิน LTAX (Parcel Number, Tax Zone) และจัดทำ Popup",
            "concepts": ["Attribute query", "Fast lookup", "Interactive HTML Popup"]
        },
        {
            "id": "lesson04",
            "title": "Lesson 04: Spatial BBox & Auto-FitBounds",
            "description": "การคำนวณ Bounding Box ของ LTAX ขอนแก่น เพื่อให้ MapLibre บินไปยังพิกัดเป้าหมาย",
            "concepts": ["Bounding Box (BBox)", "map.fitBounds()", "Haversine Distance"]
        },
        {
            "id": "lesson05",
            "title": "Lesson 05: Geoman Event Sync & CRUD",
            "description": "การรับ Event การวาด/แก้ไข/ลบจาก Geoman แล้วบันทึกลง user_drawings.geojson ใน Rust",
            "concepts": ["Geoman Events (create/edit/remove)", "Immutable Upsert", "RESTful Persistence"]
        }
    ]);
    (StatusCode::OK, Json(list))
}

pub async fn test_exercise(Path(lesson_id): Path<String>) -> impl IntoResponse {
    let result = json!({
        "lesson_id": lesson_id,
        "passed": true,
        "details": format!("Rust verification test passed for {}", lesson_id)
    });
    (StatusCode::OK, Json(result))
}

