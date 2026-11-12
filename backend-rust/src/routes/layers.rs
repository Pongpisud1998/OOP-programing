use axum::{
    extract::Path,
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use serde_json::json;
use crate::services::storage_service;

pub async fn list_layers() -> impl IntoResponse {
    let layers = storage_service::list_ltax_layers();
    (StatusCode::OK, Json(layers))
}

pub async fn get_layer(Path(layer_id): Path<String>) -> Result<impl IntoResponse, (StatusCode, Json<serde_json::Value>)> {
    if let Some(data) = storage_service::read_ltax_layer(&layer_id) {
        Ok((StatusCode::OK, Json(data)))
    } else {
        Err((
            StatusCode::NOT_FOUND,
            Json(json!({"error": format!("Layer '{}' not found in LTAX GeoJSON", layer_id)})),
        ))
    }
}

