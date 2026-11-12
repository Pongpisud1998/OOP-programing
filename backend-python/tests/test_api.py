import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["backend"] == "python-fastapi"

def test_list_dpt_layers():
    response = client.get("/api/layers")
    assert response.status_code == 200
    layers = response.json()
    assert isinstance(layers, list)
    layer_ids = [l["id"] for l in layers]
    assert "user_drawings" in layer_ids
    assert "boundary" in layer_ids
    assert "be_parcel" in layer_ids

def test_get_dpt_shapefile_boundary():
    response = client.get("/api/layers/boundary")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 0
    assert "bbox" in data

def test_get_dpt_shapefile_parcel():
    response = client.get("/api/layers/be_parcel")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 0

def test_crud_user_drawings():
    # 1. Create
    test_feature = {
        "type": "Feature",
        "id": "pytest-dpt-1",
        "properties": {"name": "New Drawn Area", "type": "park"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[100.056, 6.614], [100.058, 6.614], [100.058, 6.616], [100.056, 6.614]]]
        }
    }
    create_res = client.post("/api/features", json=test_feature)
    assert create_res.status_code == 200
    
    # 2. Update
    test_feature["properties"]["name"] = "Updated Area"
    update_res = client.put("/api/features/pytest-dpt-1", json=test_feature)
    assert update_res.status_code == 200
    assert update_res.json()["feature"]["properties"]["name"] == "Updated Area"

    # 3. Delete
    del_res = client.delete("/api/features/pytest-dpt-1")
    assert del_res.status_code == 200

def test_reset_user_drawings():
    # The frontend calls /api/reset; /api/features/reset is the older path.
    for path in ["/api/reset", "/api/features/reset"]:
        response = client.post(path)
        assert response.status_code == 200
        assert response.json()["data"]["features"] == []

