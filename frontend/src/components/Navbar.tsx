import React from 'react';
import { BackendType, BACKENDS } from '../services/api';
import { MapPin, Server, Layers, BookOpen, RefreshCw, ZoomIn } from 'lucide-react';

interface NavbarProps {
  currentBackend: BackendType;
  onSelectBackend: (backend: BackendType) => void;
  isHealthy: boolean;
  activeTab: 'map' | 'lessons';
  setActiveTab: (tab: 'map' | 'lessons') => void;
  onResetDrawings: () => void;
  onFitBounds: () => void;
  isLoading: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentBackend,
  onSelectBackend,
  isHealthy,
  activeTab,
  setActiveTab,
  onResetDrawings,
  onFitBounds,
  isLoading,
}) => {
  const currentConfig = BACKENDS[currentBackend];

  return (
    <header className="h-14 bg-slate-900/90 backdrop-blur border-b border-slate-800 px-4 flex items-center justify-between z-30 select-none">
      {/* Brand & Title */}
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <MapPin className="w-4 h-4 text-white" />
        </div>
        <div>
          <h1 className="text-sm font-bold text-white tracking-wide flex items-center gap-2">
            MapLibre GIS Studio
            <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
              v2.0
            </span>
          </h1>
          <p className="text-[11px] text-slate-400">
            {currentConfig.datasetName} • {currentConfig.location}
          </p>
        </div>
      </div>

      {/* Backend Switcher */}
      <div className="flex items-center space-x-2 bg-slate-950 p-1 rounded-xl border border-slate-800">
        <button
          onClick={() => onSelectBackend('rust')}
          className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
            currentBackend === 'rust'
              ? 'bg-amber-600/90 text-white shadow-md shadow-amber-600/30 font-semibold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
          <span>🦀 Rust (LTAX ขอนแก่น)</span>
          <span className="text-[10px] opacity-75 font-mono">:8080</span>
        </button>

        <button
          onClick={() => onSelectBackend('python')}
          className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
            currentBackend === 'python'
              ? 'bg-emerald-600/90 text-white shadow-md shadow-emerald-600/30 font-semibold'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
          }`}
        >
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>🐍 FastAPI (DPT สตูล)</span>
          <span className="text-[10px] opacity-75 font-mono">:8000</span>
        </button>
      </div>

      {/* Quick Tools & Navigation */}
      <div className="flex items-center space-x-2">
        {/* Server Status Pill */}
        <div className="hidden md:flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-mono bg-slate-800 border border-slate-700">
          <Server className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-300">Port {currentConfig.port}</span>
          <span
            className={`w-2 h-2 rounded-full ${
              isHealthy ? 'bg-emerald-500 shadow-sm shadow-emerald-500' : 'bg-rose-500 animate-ping'
            }`}
          />
        </div>

        {/* Fit Bounds Button */}
        <button
          onClick={onFitBounds}
          title="Zoom to Data Extent"
          className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition"
        >
          <ZoomIn className="w-4 h-4" />
        </button>

        {/* Reset Drawings Button */}
        <button
          onClick={onResetDrawings}
          title="Reset User Drawings on Active Backend"
          className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-rose-400 border border-slate-700 transition flex items-center gap-1 text-xs"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin text-blue-400' : ''}`} />
          <span className="hidden sm:inline">Reset Drawings</span>
        </button>

        {/* Tab Switcher (Map vs Lessons) */}
        <div className="flex items-center bg-slate-800 p-0.5 rounded-lg border border-slate-700">
          <button
            onClick={() => setActiveTab('map')}
            className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs transition ${
              activeTab === 'map' ? 'bg-blue-600 text-white font-medium' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Map Studio</span>
          </button>
          <button
            onClick={() => setActiveTab('lessons')}
            className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs transition ${
              activeTab === 'lessons' ? 'bg-blue-600 text-white font-medium' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>บทเรียน & แบบฝึกหัด</span>
          </button>
        </div>
      </div>
    </header>
  );
};

