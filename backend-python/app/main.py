from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import layers, features

app = FastAPI(
    title="DPT GIS API (Python FastAPI)",
    description="Backend API for DPT Shapefile layers in Satun and Geoman CRUD",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(layers.router)
app.include_router(features.router)

# The frontend and the Rust backend both use /api/reset; keep /api/features/reset as an alias.
app.add_api_route("/api/reset", features.reset_features, methods=["POST"], tags=["Features"])

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "backend": "python-fastapi",
        "dataset": "DPT Shapefile (Satun)",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

