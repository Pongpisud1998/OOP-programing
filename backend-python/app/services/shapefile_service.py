import os
import zipfile
import json
from typing import Dict, Any, List, Optional
import shapefile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/dpt/shapefile"))
EXTRACTED_DIR = os.path.join(BASE_DIR, "extracted")
USER_DRAWINGS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/dpt/user_drawings.geojson"))

def ensure_extracted():
    """Extract any .zip shapefiles if not already extracted."""
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    if not os.path.exists(BASE_DIR):
        return

    for item in os.listdir(BASE_DIR):
        if item.endswith(".zip"):
            stem = item[:-4]
            target_folder = os.path.join(EXTRACTED_DIR, stem)
            shp_target = os.path.join(target_folder, f"{stem}.shp")
            if not os.path.exists(shp_target):
                os.makedirs(target_folder, exist_ok=True)
                zip_path = os.path.join(BASE_DIR, item)
                try:
                    with zipfile.ZipFile(zip_path, "r") as z:
                        z.extractall(target_folder)
                except Exception as e:
                    print(f"Error extracting {item}: {e}")

def list_dpt_layers() -> List[Dict[str, Any]]:
    """List all available DPT shapefile layers and the user drawings layer."""
    ensure_extracted()
    layers = []

    # 1. User drawings layer
    user_count = 0
    if os.path.exists(USER_DRAWINGS_FILE):
        try:
            with open(USER_DRAWINGS_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                user_count = len(d.get("features", []))
        except Exception:
            pass

    layers.append({
        "id": "user_drawings",
        "name": "User Drawings (ชั้นข้อมูลที่วาด/แก้ไข)",
        "type": "geojson",
        "source": "dpt",
        "editable": True,
        "feature_count": user_count,
        "geometry_types": ["Point", "LineString", "Polygon"],
        "color": "#ef4444",
        "bbox": [100.055, 6.613, 100.065, 6.620]
    })

    # 2. Shapefile layers
    if os.path.exists(EXTRACTED_DIR):
        for item in sorted(os.listdir(EXTRACTED_DIR)):
            folder = os.path.join(EXTRACTED_DIR, item)
            if os.path.isdir(folder):
                shp_path = os.path.join(folder, f"{item}.shp")
                if os.path.exists(shp_path):
                    try:
                        sf = shapefile.Reader(shp_path, encoding="utf-8")
                        bbox = [round(b, 6) for b in sf.bbox] if sf.bbox else [100.055, 6.613, 100.065, 6.620]
                        
                        layer_name_map = {
                            "boundary": "DPT: ขอบเขตผังเมืองรวมสตูล (Boundary)",
                            "be_parcel": "DPT: แปลงที่ดิน (Parcel)",
                            "be_public": "DPT: ที่ดินสาธารณประโยชน์ (Public Land)",
                            "af_public": "DPT: พื้นที่สาธารณูปโภค (Public Utility)"
                        }
                        color_map = {
                            "boundary": "#dc2626",
                            "be_parcel": "#2563eb",
                            "be_public": "#16a34a",
                            "af_public": "#d97706"
                        }

                        layers.append({
                            "id": item,
                            "name": layer_name_map.get(item, f"DPT: {item}"),
                            "type": "shapefile",
                            "source": "dpt",
                            "editable": False,
                            "feature_count": len(sf),
                            "geometry_types": [sf.shapeTypeName],
                            "color": color_map.get(item, "#6366f1"),
                            "bbox": bbox
                        })
                    except Exception as e:
                        print(f"Error reading shapefile {shp_path}: {e}")

    return layers

def read_dpt_shapefile(layer_id: str) -> Dict[str, Any]:
    """Read a DPT shapefile and return standard GeoJSON FeatureCollection."""
    ensure_extracted()
    shp_path = os.path.join(EXTRACTED_DIR, layer_id, f"{layer_id}.shp")
    if not os.path.exists(shp_path):
        raise FileNotFoundError(f"Shapefile '{layer_id}' not found")

    with shapefile.Reader(shp_path, encoding="utf-8") as sf:
        fields = [f[0] for f in sf.fields[1:]]
        features = []

        for idx, sr in enumerate(sf.shapeRecords()):
            geom = sr.shape.__geo_interface__
            # Clean records
            rec_dict = {}
            for k, v in zip(fields, sr.record):
                if isinstance(v, bytes):
                    try:
                        v = v.decode("utf-8")
                    except UnicodeDecodeError:
                        v = v.decode("cp874", errors="ignore")
                rec_dict[k] = v

            feat_id = str(rec_dict.get("id") or f"{layer_id}-{idx + 1}")
            features.append({
                "type": "Feature",
                "id": feat_id,
                "properties": rec_dict,
                "geometry": geom
            })

        bbox = [round(b, 6) for b in sf.bbox] if sf.bbox else [100.055, 6.613, 100.065, 6.620]
        return {
            "type": "FeatureCollection",
            "name": layer_id,
            "bbox": bbox,
            "features": features
        }

# User Drawings CRUD
def read_user_drawings() -> Dict[str, Any]:
    if not os.path.exists(USER_DRAWINGS_FILE):
        empty = {"type": "FeatureCollection", "name": "dpt_user_drawings", "features": []}
        with open(USER_DRAWINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(empty, f, indent=2, ensure_ascii=False)
        return empty

    with open(USER_DRAWINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user_drawings(data: Dict[str, Any]) -> None:
    with open(USER_DRAWINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_user_feature(feature: Dict[str, Any]) -> Dict[str, Any]:
    data = read_user_drawings()
    if "id" not in feature or not feature["id"]:
        import uuid
        feature["id"] = f"dpt_draw_{uuid.uuid4().hex[:8]}"
    if "properties" not in feature:
        feature["properties"] = {}
    
    data.setdefault("features", []).append(feature)
    save_user_drawings(data)
    return feature

def update_user_feature(feature_id: str, updated_feature: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    data = read_user_drawings()
    features = data.get("features", [])
    found = False
    for i, feat in enumerate(features):
        if str(feat.get("id")) == str(feature_id):
            updated_feature["id"] = feature_id
            features[i] = updated_feature
            found = True
            break
    if found:
        data["features"] = features
        save_user_drawings(data)
        return updated_feature
    return None

def delete_user_feature(feature_id: str) -> bool:
    data = read_user_drawings()
    features = data.get("features", [])
    initial_len = len(features)
    new_features = [f for f in features if str(f.get("id")) != str(feature_id)]
    if len(new_features) < initial_len:
        data["features"] = new_features
        save_user_drawings(data)
        return True
    return False

def reset_user_drawings() -> Dict[str, Any]:
    empty = {"type": "FeatureCollection", "name": "dpt_user_drawings", "features": []}
    save_user_drawings(empty)
    return empty

