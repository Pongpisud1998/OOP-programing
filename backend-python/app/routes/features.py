from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..services import shapefile_service

router = APIRouter(prefix="/api/features", tags=["Features"])

@router.post("")
def create_feature(feature: Dict[str, Any]):
    """Add a newly drawn feature to DPT user drawings."""
    if "type" not in feature or feature.get("type") != "Feature":
        raise HTTPException(status_code=400, detail="Invalid GeoJSON Feature format")
    if "geometry" not in feature or not feature["geometry"]:
        raise HTTPException(status_code=400, detail="Feature must contain geometry")

    saved = shapefile_service.add_user_feature(feature)
    return {"status": "success", "message": "Feature added to DPT drawings", "feature": saved}

@router.put("/{feature_id}")
def update_feature(feature_id: str, feature: Dict[str, Any]):
    """Update geometry or properties of a feature in DPT drawings."""
    updated = shapefile_service.update_user_feature(feature_id, feature)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Feature '{feature_id}' not found")
    return {"status": "success", "message": "Feature updated", "feature": updated}

@router.delete("/{feature_id}")
def delete_feature(feature_id: str):
    """Delete a feature by its id from DPT drawings."""
    success = shapefile_service.delete_user_feature(feature_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Feature '{feature_id}' not found")
    return {"status": "success", "message": f"Feature '{feature_id}' deleted"}

@router.post("/reset")
def reset_features():
    """Reset DPT user drawings."""
    data = shapefile_service.reset_user_drawings()
    return {"status": "success", "message": "DPT user drawings reset", "data": data}

