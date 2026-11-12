use serde_json::{json, Value};
use std::fs;
use std::path::{Path, PathBuf};

pub fn get_ltax_dir() -> PathBuf {
    Path::new("../data/ltax/geojson").canonicalize().unwrap_or_else(|_| PathBuf::from("../data/ltax/geojson"))
}

pub fn get_user_drawings_file() -> PathBuf {
    Path::new("../data/ltax/user_drawings.geojson").canonicalize().unwrap_or_else(|_| PathBuf::from("../data/ltax/user_drawings.geojson"))
}

pub fn list_ltax_layers() -> Vec<Value> {
    let mut layers = Vec::new();

    // 1. User Drawings layer
    let user_drawings = read_user_drawings();
    let user_count = user_drawings.get("features").and_then(|f| f.as_array()).map_or(0, |a| a.len());
    layers.push(json!({
        "id": "user_drawings",
        "name": "User Drawings (ชั้นข้อมูลที่วาด/แก้ไข)",
        "type": "geojson",
        "source": "ltax",
        "editable": true,
        "feature_count": user_count,
        "geometry_types": ["Point", "LineString", "Polygon"],
        "color": "#ef4444",
        "bbox": [102.158, 16.588, 102.352, 16.690]
    }));

    // 2. LTAX GeoJSON layers
    let ltax_dir = get_ltax_dir();
    let _layer_order = ["boundary", "zone", "block", "parcel", "building"];
    let name_map = [
        ("boundary", "LTAX: ขอบเขตองค์กรปกครองส่วนท้องถิ่น (Boundary)", "#dc2626"),
        ("zone", "LTAX: โซนผังภาษี (Tax Zone)", "#8b5cf6"),
        ("block", "LTAX: บล็อกผังภาษี (Tax Block)", "#3b82f6"),
        ("parcel", "LTAX: แปลงที่ดิน (Tax Parcel)", "#059669"),
        ("building", "LTAX: โรงเรือนและสิ่งปลูกสร้าง (Building)", "#d97706"),
    ];

    for (id, display_name, color) in name_map {
        let file_path = ltax_dir.join(format!("{}.geojson", id));
        if file_path.exists() {
            let mut count = 0;
            let mut geom_types = Vec::new();
            if let Ok(content) = fs::read_to_string(&file_path) {
                if let Ok(val) = serde_json::from_str::<Value>(&content) {
                    if let Some(features) = val.get("features").and_then(|f| f.as_array()) {
                        count = features.len();
                        for f in features.iter().take(20) {
                            if let Some(gt) = f.get("geometry").and_then(|g| g.get("type")).and_then(|t| t.as_str()) {
                                let s = gt.to_string();
                                if !geom_types.contains(&s) {
                                    geom_types.push(s);
                                }
                            }
                        }
                    }
                }
            }

            layers.push(json!({
                "id": id,
                "name": display_name,
                "type": "geojson",
                "source": "ltax",
                "editable": false,
                "feature_count": count,
                "geometry_types": geom_types,
                "color": color,
                "bbox": [102.158, 16.588, 102.352, 16.690]
            }));
        }
    }

    layers
}

pub fn read_ltax_layer(layer_id: &str) -> Option<Value> {
    if layer_id == "user_drawings" || layer_id == "ltax_user_drawings" {
        return Some(read_user_drawings());
    }

    let ltax_dir = get_ltax_dir();
    let file_path = ltax_dir.join(format!("{}.geojson", layer_id));
    if file_path.exists() {
        let content = fs::read_to_string(file_path).ok()?;
        serde_json::from_str(&content).ok()
    } else {
        None
    }
}

pub fn read_user_drawings() -> Value {
    let file = get_user_drawings_file();
    if !file.exists() {
        let empty = json!({
            "type": "FeatureCollection",
            "name": "ltax_user_drawings",
            "features": []
        });
        let _ = fs::write(&file, serde_json::to_string_pretty(&empty).unwrap());
        return empty;
    }

    let content = fs::read_to_string(&file).unwrap_or_default();
    serde_json::from_str(&content).unwrap_or_else(|_| json!({
        "type": "FeatureCollection",
        "name": "ltax_user_drawings",
        "features": []
    }))
}

pub fn save_user_drawings(val: &Value) -> Result<(), String> {
    let file = get_user_drawings_file();
    let formatted = serde_json::to_string_pretty(val).map_err(|e| e.to_string())?;
    fs::write(file, formatted).map_err(|e| e.to_string())
}

pub fn add_user_feature(mut feature: Value) -> Result<Value, String> {
    let mut data = read_user_drawings();
    let features_arr = data.get_mut("features")
        .and_then(|f| f.as_array_mut())
        .ok_or("Features array missing")?;

    if feature.get("id").is_none() || feature.get("id").unwrap().is_null() {
        let id = format!("ltax_draw_{}", &uuid_v4_simple()[..8]);
        feature["id"] = json!(id);
    }
    if feature.get("properties").is_none() {
        feature["properties"] = json!({});
    }

    features_arr.push(feature.clone());
    save_user_drawings(&data)?;
    Ok(feature)
}

pub fn update_user_feature(feature_id: &str, mut feature: Value) -> Result<Value, String> {
    let mut data = read_user_drawings();
    let features_arr = data.get_mut("features")
        .and_then(|f| f.as_array_mut())
        .ok_or("Features array missing")?;

    let mut found = false;
    for item in features_arr.iter_mut() {
        if item.get("id").map_or(false, |id| id.as_str().unwrap_or("") == feature_id || id.to_string() == feature_id) {
            feature["id"] = json!(feature_id);
            *item = feature.clone();
            found = true;
            break;
        }
    }

    if found {
        save_user_drawings(&data)?;
        Ok(feature)
    } else {
        Err(format!("Feature '{}' not found", feature_id))
    }
}

pub fn delete_user_feature(feature_id: &str) -> Result<(), String> {
    let mut data = read_user_drawings();
    let features_arr = data.get_mut("features")
        .and_then(|f| f.as_array_mut())
        .ok_or("Features array missing")?;

    let initial_len = features_arr.len();
    features_arr.retain(|item| {
        !item.get("id").map_or(false, |id| id.as_str().unwrap_or("") == feature_id || id.to_string() == feature_id)
    });

    if features_arr.len() < initial_len {
        save_user_drawings(&data)?;
        Ok(())
    } else {
        Err(format!("Feature '{}' not found", feature_id))
    }
}

pub fn reset_user_drawings() -> Result<Value, String> {
    let empty = json!({
        "type": "FeatureCollection",
        "name": "ltax_user_drawings",
        "features": []
    });
    save_user_drawings(&empty)?;
    Ok(empty)
}

fn uuid_v4_simple() -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let nanos = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
    format!("{:x}", nanos)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_list_ltax_layers() {
        let layers = list_ltax_layers();
        assert!(!layers.is_empty());
        let ids: Vec<String> = layers.iter().map(|l| l["id"].as_str().unwrap().to_string()).collect();
        assert!(ids.contains(&"user_drawings".to_string()));
        assert!(ids.contains(&"boundary".to_string()));
        assert!(ids.contains(&"parcel".to_string()));
    }

    #[test]
    fn test_user_drawings_crud() {
        let test_feat = json!({
            "type": "Feature",
            "id": "rust_test_1",
            "properties": { "name": "Rust Zone" },
            "geometry": {
                "type": "Point",
                "coordinates": [102.25, 16.65]
            }
        });

        let added = add_user_feature(test_feat.clone()).unwrap();
        assert_eq!(added["id"], "rust_test_1");

        let updated_feat = json!({
            "type": "Feature",
            "id": "rust_test_1",
            "properties": { "name": "Rust Zone Updated" },
            "geometry": {
                "type": "Point",
                "coordinates": [102.26, 16.66]
            }
        });
        let updated = update_user_feature("rust_test_1", updated_feat).unwrap();
        assert_eq!(updated["properties"]["name"], "Rust Zone Updated");

        let del_res = delete_user_feature("rust_test_1");
        assert!(del_res.is_ok());
    }
}
