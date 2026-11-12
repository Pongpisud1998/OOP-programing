use axum::{
    extract::Path,
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use serde_json::{json, Value};
use crate::services::storage_service;

pub async fn create_feature(Json(payload): Json<Value>) -> Result<impl IntoResponse, (StatusCode, Json<Value>)> {
    if payload.get("type").and_then(|t| t.as_str()) != Some("Feature") {
        return Err((StatusCode::BAD_REQUEST, Json(json!({"error": "Invalid GeoJSON Feature format"}))));
    }
    if payload.get("geometry").is_none() {
        return Err((StatusCode::BAD_REQUEST, Json(json!({"error": "Feature must contain geometry"}))));
    }

    match storage_service::add_user_feature(payload) {
        Ok(feat) => Ok((StatusCode::OK, Json(json!({
            "status": "success",
            "message": "Feature added to LTAX drawings",
            "feature": feat
        })))),
        Err(e) => Err((StatusCode::INTERNAL_SERVER_ERROR, Json(json!({"error": e})))),
    }
}

pub async fn update_feature(
    Path(feature_id): Path<String>,
    Json(payload): Json<Value>,
) -> Result<impl IntoResponse, (StatusCode, Json<Value>)> {
    match storage_service::update_user_feature(&feature_id, payload) {
        Ok(updated) => Ok((StatusCode::OK, Json(json!({
            "status": "success",
            "message": "Feature updated",
            "feature": updated
        })))),
        Err(e) => Err((StatusCode::NOT_FOUND, Json(json!({"error": e})))),
    }
}

pub async fn delete_feature(Path(feature_id): Path<String>) -> Result<impl IntoResponse, (StatusCode, Json<Value>)> {
    match storage_service::delete_user_feature(&feature_id) {
        Ok(_) => Ok((StatusCode::OK, Json(json!({
            "status": "success",
            "message": format!("Feature '{}' deleted", feature_id)
        })))),
        Err(e) => Err((StatusCode::NOT_FOUND, Json(json!({"error": e})))),
    }
}

pub async fn reset_features() -> Result<impl IntoResponse, (StatusCode, Json<Value>)> {
    match storage_service::reset_user_drawings() {
        Ok(data) => Ok((StatusCode::OK, Json(json!({
            "status": "success",
            "message": "LTAX user drawings reset",
            "data": data
        })))),
        Err(e) => Err((StatusCode::INTERNAL_SERVER_ERROR, Json(json!({"error": e})))),
    }
}

