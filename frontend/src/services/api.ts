export type BackendType = 'rust' | 'python';

export interface LayerMetadata {
  id: string;
  name: string;
  type: string;
  source: 'ltax' | 'dpt';
  editable: boolean;
  feature_count: number | null;
  geometry_types: string[];
  color: string;
  bbox?: [number, number, number, number];
}

export interface BackendConfig {
  type: BackendType;
  name: string;
  port: number;
  url: string;
  datasetName: string;
  location: string;
  defaultBBox: [number, number, number, number];
}

export const BACKENDS: Record<BackendType, BackendConfig> = {
  rust: {
    type: 'rust',
    name: 'Rust (Axum)',
    port: 8080,
    url: 'http://localhost:8080',
    datasetName: 'LTAX GeoJSON',
    location: 'ขอนแก่น (Khon Kaen)',
    defaultBBox: [102.158, 16.588, 102.352, 16.690],
  },
  python: {
    type: 'python',
    name: 'Python (FastAPI)',
    port: 8000,
    url: 'http://localhost:8000',
    datasetName: 'DPT Shapefile (Zip)',
    location: 'สตูล (Satun)',
    defaultBBox: [100.055, 6.613, 100.065, 6.620],
  },
};

export class ApiService {
  private currentBackend: BackendType = 'python';

  setBackend(backend: BackendType) {
    this.currentBackend = backend;
  }

  getBackend(): BackendType {
    return this.currentBackend;
  }

  getConfig(): BackendConfig {
    return BACKENDS[this.currentBackend];
  }

  private getBaseUrl(): string {
    return BACKENDS[this.currentBackend].url;
  }

  async checkHealth(): Promise<{ status: string; backend: string; dataset?: string; healthy: boolean }> {
    try {
      const res = await fetch(`${this.getBaseUrl()}/api/health`, { signal: AbortSignal.timeout(3000) });
      if (!res.ok) throw new Error('Not healthy');
      const data = await res.json();
      return { ...data, healthy: true };
    } catch {
      return { status: 'offline', backend: this.currentBackend, healthy: false };
    }
  }

  async getLayers(): Promise<LayerMetadata[]> {
    const res = await fetch(`${this.getBaseUrl()}/api/layers`);
    if (!res.ok) throw new Error(`Failed to load layers from ${this.currentBackend}`);
    return res.json();
  }

  async getLayerGeoJSON(layerId: string): Promise<any> {
    const res = await fetch(`${this.getBaseUrl()}/api/layers/${layerId}`);
    if (!res.ok) throw new Error(`Failed to load GeoJSON for ${layerId}`);
    return res.json();
  }

  async createFeature(feature: any): Promise<any> {
    const res = await fetch(`${this.getBaseUrl()}/api/features`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feature),
    });
    if (!res.ok) throw new Error('Failed to create feature');
    return res.json();
  }

  async updateFeature(featureId: string, feature: any): Promise<any> {
    const res = await fetch(`${this.getBaseUrl()}/api/features/${featureId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feature),
    });
    if (!res.ok) throw new Error('Failed to update feature');
    return res.json();
  }

  async deleteFeature(featureId: string): Promise<any> {
    const res = await fetch(`${this.getBaseUrl()}/api/features/${featureId}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete feature');
    return res.json();
  }

  async resetFeatures(): Promise<any> {
    const res = await fetch(`${this.getBaseUrl()}/api/reset`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to reset features');
    return res.json();
  }
}

export const api = new ApiService();

