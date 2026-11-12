import React from 'react';
import { LayerMetadata } from '../services/api';
import { Eye, EyeOff, Layers, Sliders, MapPin, Hash, Sparkles } from 'lucide-react';

interface LayerManagerProps {
  layers: LayerMetadata[];
  layerVisibility: Record<string, boolean>;
  layerOpacity: Record<string, number>;
  onToggleVisibility: (layerId: string) => void;
  onChangeOpacity: (layerId: string, opacity: number) => void;
  onZoomToLayer?: (layer: LayerMetadata) => void;
}

export const LayerManager: React.FC<LayerManagerProps> = ({
  layers,
  layerVisibility,
  layerOpacity,
  onToggleVisibility,
  onChangeOpacity,
  onZoomToLayer,
}) => {
  return (
    <div className="w-80 bg-slate-900/95 backdrop-blur border-r border-slate-800 flex flex-col h-full z-20 shadow-2xl">
      {/* Header */}
      <div className="p-3 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Layers className="w-4 h-4 text-blue-400" />
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-200">
            Layer Manager ({layers.length})
          </h2>
        </div>
        <span className="text-[10px] text-slate-400 font-mono">MapLibre GL</span>
      </div>

      {/* Layer List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
        {layers.map((layer) => {
          const isVisible = layerVisibility[layer.id] ?? true;
          const opacity = layerOpacity[layer.id] ?? 0.8;

          return (
            <div
              key={layer.id}
              className={`p-3 rounded-xl border transition-all ${
                isVisible
                  ? 'bg-slate-800/80 border-slate-700/80 shadow-sm'
                  : 'bg-slate-900/40 border-slate-800/50 opacity-60'
              }`}
            >
              {/* Layer Title Row */}
              <div className="flex items-start justify-between gap-2 mb-2">
                <div className="flex items-center space-x-2">
                  <div
                    className="w-3.5 h-3.5 rounded shadow-sm border border-black/20 flex-shrink-0"
                    style={{ backgroundColor: layer.color }}
                  />
                  <div>
                    <h3 className="text-xs font-semibold text-slate-100 flex items-center gap-1.5 leading-snug">
                      {layer.name}
                      {layer.editable && (
                        <span className="text-[9px] px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 flex items-center gap-0.5">
                          <Sparkles className="w-2.5 h-2.5" /> Editable
                        </span>
                      )}
                    </h3>
                    <p className="text-[10px] text-slate-400 flex items-center gap-2 mt-0.5">
                      <span className="flex items-center gap-0.5 font-mono">
                        <Hash className="w-2.5 h-2.5" />
                        {layer.feature_count !== null ? `${layer.feature_count} features` : 'Dynamic'}
                      </span>
                      <span>•</span>
                      <span className="capitalize">{layer.type}</span>
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-1">
                  {layer.bbox && onZoomToLayer && (
                    <button
                      onClick={() => onZoomToLayer(layer)}
                      title="Zoom to this layer"
                      className="p-1 rounded hover:bg-slate-700 text-slate-400 hover:text-blue-400 transition"
                    >
                      <MapPin className="w-3.5 h-3.5" />
                    </button>
                  )}
                  <button
                    onClick={() => onToggleVisibility(layer.id)}
                    title={isVisible ? 'Hide Layer' : 'Show Layer'}
                    className={`p-1 rounded transition ${
                      isVisible
                        ? 'text-blue-400 hover:bg-slate-700'
                        : 'text-slate-500 hover:bg-slate-800'
                    }`}
                  >
                    {isVisible ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>

              {/* Opacity Slider */}
              {isVisible && (
                <div className="mt-2.5 pt-2 border-t border-slate-700/50 flex items-center justify-between space-x-2">
                  <div className="flex items-center space-x-1.5 text-slate-400">
                    <Sliders className="w-3 h-3" />
                    <span className="text-[10px] font-mono">Opacity</span>
                  </div>
                  <div className="flex items-center space-x-2 flex-1 max-w-[140px]">
                    <input
                      type="range"
                      min="0.1"
                      max="1.0"
                      step="0.05"
                      value={opacity}
                      onChange={(e) => onChangeOpacity(layer.id, parseFloat(e.target.value))}
                      className="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                    />
                    <span className="text-[10px] text-slate-400 font-mono w-7 text-right">
                      {Math.round(opacity * 100)}%
                    </span>
                  </div>
                </div>
              )}
            </div>
          );
        })}

        {layers.length === 0 && (
          <div className="p-4 text-center text-xs text-slate-500">
            กำลังโหลดข้อมูลเลเยอร์ หรือ Backend ออฟไลน์...
          </div>
        )}
      </div>

      {/* Footer Info */}
      <div className="p-3 bg-slate-950/60 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
        <span>💡 คลิกที่รูปทรงบนแผนที่เพื่อดูข้อมูล Attribute</span>
      </div>
    </div>
  );
};

