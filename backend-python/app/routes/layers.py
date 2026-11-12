from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ..services import shapefile_service

router = APIRouter(prefix="/api/layers", tags=["Layers"])

@router.get("", response_model=List[Dict[str, Any]])
def get_all_layers():
    """List all available DPT layers (Shapefiles and User Drawings)."""
    return shapefile_service.list_dpt_layers()

@router.get("/{layer_id}")
def get_layer_geojson(layer_id: str):
    """
    Fetch GeoJSON FeatureCollection for a DPT layer.
    """
    if layer_id in ["user_drawings", "dpt_user_drawings"]:
        return shapefile_service.read_user_drawings()

    try:
        return shapefile_service.read_dpt_shapefile(layer_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Layer '{layer_id}' not found in DPT shapefiles")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading shapefile: {str(e)}")

