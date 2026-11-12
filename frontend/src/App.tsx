import React, { useState, useEffect, useCallback } from 'react';
import { api, BackendType, BACKENDS, LayerMetadata } from './services/api';
import { Navbar } from './components/Navbar';
import { LayerManager } from './components/LayerManager';
import { MapView } from './components/MapView';
import { LearningSidebar } from './components/LearningSidebar';

export default function App() {
  const [currentBackend, setCurrentBackend] = useState<BackendType>('python');
  const [isHealthy, setIsHealthy] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'map' | 'lessons'>('map');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Layer states
  const [layers, setLayers] = useState<LayerMetadata[]>([]);
  const [layerData, setLayerData] = useState<Record<string, any>>({});
  const [layerVisibility, setLayerVisibility] = useState<Record<string, boolean>>({});
  const [layerOpacity, setLayerOpacity] = useState<Record<string, number>>({});
  const [notification, setNotification] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

  const showNotification = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3500);
  };

  // Check health and load layers on backend switch or mount
  const loadBackendData = useCallback(async (backend: BackendType) => {
    setIsLoading(true);
    api.setBackend(backend);
    setCurrentBackend(backend);

    try {
      const health = await api.checkHealth();
      setIsHealthy(health.healthy);

      if (health.healthy) {
        const layerList = await api.getLayers();
        setLayers(layerList);

        // Fetch GeoJSON data for all layers
        const dataMap: Record<string, any> = {};
        const visMap: Record<string, boolean> = {};
        const opMap: Record<string, number> = {};

        await Promise.all(
          layerList.map(async (l) => {
            visMap[l.id] = true;
            opMap[l.id] = l.id === 'boundary' ? 1.0 : l.editable ? 0.9 : 0.6;
            try {
              const geojson = await api.getLayerGeoJSON(l.id);
              dataMap[l.id] = geojson;
            } catch (err) {
              console.error(`Failed to load GeoJSON for layer ${l.id}:`, err);
            }
          })
        );

        setLayerData(dataMap);
        setLayerVisibility(visMap);
        setLayerOpacity(opMap);

        showNotification(
          `เชื่อมต่อ ${BACKENDS[backend].name} สำเร็จ! โหลด ${layerList.length} ชั้นข้อมูล (${BACKENDS[backend].location})`,
          'success'
        );
      } else {
        showNotification(`ไม่พบเซิร์ฟเวอร์ ${BACKENDS[backend].name} ที่พอร์ต ${BACKENDS[backend].port}`, 'error');
      }
    } catch (err: any) {
      showNotification(`เกิดข้อผิดพลาด: ${err.message}`, 'error');
      setIsHealthy(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadBackendData(currentBackend);
  }, [loadBackendData]);

  // Periodic health check
  useEffect(() => {
    const timer = setInterval(async () => {
      const health = await api.checkHealth();
      setIsHealthy(health.healthy);
    }, 8000);
    return () => clearInterval(timer);
  }, [currentBackend]);

  // Layer Controls
  const handleToggleVisibility = (layerId: string) => {
    setLayerVisibility((prev) => ({
      ...prev,
      [layerId]: !prev[layerId],
    }));
  };

  const handleChangeOpacity = (layerId: string, opacity: number) => {
    setLayerOpacity((prev) => ({
      ...prev,
      [layerId]: opacity,
    }));
  };

  // Geoman Feature CRUD
  const handleFeatureCreated = async (feature: any) => {
    try {
      const res = await api.createFeature(feature);
      showNotification(`บันทึกรูปทรงใหม่ลง ${BACKENDS[currentBackend].name} เรียบร้อย!`, 'success');
      // Refresh user drawings layer
      const updated = await api.getLayerGeoJSON('user_drawings');
      setLayerData((prev) => ({ ...prev, user_drawings: updated }));
    } catch (err: any) {
      showNotification(`บันทึกไม่สำเร็จ: ${err.message}`, 'error');
    }
  };

  const handleFeatureUpdated = async (feature: any) => {
    const featId = feature.id || feature?.properties?.id;
    if (!featId) return;
    try {
      await api.updateFeature(featId, feature);
      showNotification(`อัปเดตรูปทรง #${featId} เรียบร้อย!`, 'info');
      const updated = await api.getLayerGeoJSON('user_drawings');
      setLayerData((prev) => ({ ...prev, user_drawings: updated }));
    } catch (err: any) {
      showNotification(`อัปเดตไม่สำเร็จ: ${err.message}`, 'error');
    }
  };

  const handleFeatureDeleted = async (featureId: string) => {
    try {
      await api.deleteFeature(featureId);
      showNotification(`ลบรูปทรง #${featureId} ออกจากระบบแล้ว`, 'info');
      const updated = await api.getLayerGeoJSON('user_drawings');
      setLayerData((prev) => ({ ...prev, user_drawings: updated }));
    } catch (err: any) {
      showNotification(`ลบไม่สำเร็จ: ${err.message}`, 'error');
    }
  };

  const handleResetDrawings = async () => {
    if (!window.confirm('คุณต้องการรีเซ็ตรูปทรงที่วาดทั้งหมดใน Backend นี้ใช่หรือไม่?')) return;
    setIsLoading(true);
    try {
      await api.resetFeatures();
      const updated = await api.getLayerGeoJSON('user_drawings');
      setLayerData((prev) => ({ ...prev, user_drawings: updated }));
      showNotification(`รีเซ็ต User Drawings ของ ${BACKENDS[currentBackend].name} เรียบร้อย!`, 'success');
    } catch (err: any) {
      showNotification(`รีเซ็ตไม่สำเร็จ: ${err.message}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const config = BACKENDS[currentBackend];

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-950 text-slate-100">
      {/* Top Navigation */}
      <Navbar
        currentBackend={currentBackend}
        onSelectBackend={(b) => loadBackendData(b)}
        isHealthy={isHealthy}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onResetDrawings={handleResetDrawings}
        onFitBounds={() => {
          // Re-trigger bbox flyto
          const prev = config.defaultBBox;
          setLayers([...layers]);
        }}
        isLoading={isLoading}
      />

      {/* Main Workspace Area */}
      <div className="flex flex-1 relative overflow-hidden">
        {/* Layer Manager Panel */}
        <LayerManager
          layers={layers}
          layerVisibility={layerVisibility}
          layerOpacity={layerOpacity}
          onToggleVisibility={handleToggleVisibility}
          onChangeOpacity={handleChangeOpacity}
        />

        {/* Center Map View */}
        <MapView
          layers={layers}
          layerData={layerData}
          layerVisibility={layerVisibility}
          layerOpacity={layerOpacity}
          defaultBBox={config.defaultBBox}
          onFeatureCreated={handleFeatureCreated}
          onFeatureUpdated={handleFeatureUpdated}
          onFeatureDeleted={handleFeatureDeleted}
        />

        {/* Right Sidebar: Learning Curriculum & Exercises */}
        {activeTab === 'lessons' && <LearningSidebar />}
      </div>

      {/* Toast Notification */}
      {notification && (
        <div
          className={`fixed bottom-5 right-5 px-4 py-2.5 rounded-xl shadow-2xl border text-xs font-medium z-50 flex items-center space-x-2 animate-bounce ${
            notification.type === 'success'
              ? 'bg-emerald-950/90 border-emerald-700 text-emerald-200'
              : notification.type === 'error'
              ? 'bg-rose-950/90 border-rose-700 text-rose-200'
              : 'bg-blue-950/90 border-blue-700 text-blue-200'
          }`}
        >
          <span>{notification.message}</span>
        </div>
      )}
    </div>
  );
}

