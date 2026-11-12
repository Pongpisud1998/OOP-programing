use axum::{
    routing::{delete, get, post, put},
    Router,
};
use std::net::SocketAddr;
use tower_http::cors::{Any, CorsLayer};

pub mod routes;
pub mod services;

#[tokio::main]
async fn main() {
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let app = Router::new()
        .route(
            "/api/health",
            get(|| async {
                axum::Json(serde_json::json!({
                    "status": "healthy",
                    "backend": "rust-axum",
                    "dataset": "LTAX GeoJSON (Khon Kaen)",
                    "version": "1.0.0"
                }))
            }),
        )
        // Layers
        .route("/api/layers", get(routes::layers::list_layers))
        .route("/api/layers/:layer_id", get(routes::layers::get_layer))
        // Features CRUD (User Drawings)
        .route("/api/features", post(routes::features::create_feature))
        .route("/api/features/:feature_id", put(routes::features::update_feature))
        .route("/api/features/:feature_id", delete(routes::features::delete_feature))
        .route("/api/reset", post(routes::features::reset_features))
        .route("/api/features/reset", post(routes::features::reset_features))
        .layer(cors);

    let addr = SocketAddr::from(([0, 0, 0, 0], 8080));
    println!("🦀 Rust Axum server running on http://localhost:8080");

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
