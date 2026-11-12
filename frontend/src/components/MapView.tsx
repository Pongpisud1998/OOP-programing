import React, { useEffect, useRef } from 'react';
import * as maplibregl from 'maplibre-gl';
import { Geoman } from '@geoman-io/maplibre-geoman-free';
import { LayerMetadata } from '../services/api';

interface MapViewProps {
  layers: LayerMetadata[];
  layerData: Record<string, any>;
  layerVisibility: Record<string, boolean>;
  layerOpacity: Record<string, number>;
  defaultBBox: [number, number, number, number];
  onFeatureCreated: (feature: any) => void;
  onFeatureUpdated: (feature: any) => void;
  onFeatureDeleted: (featureId: string) => void;
}

export const MapView: React.FC<MapViewProps> = ({
  layers,
  layerData,
  layerVisibility,
  layerOpacity,
  defaultBBox,
  onFeatureCreated,
  onFeatureUpdated,
  onFeatureDeleted,
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const geomanRef = useRef<any>(null);
  const popupRef = useRef<maplibregl.Popup | null>(null);

  // 1. Initialize MapLibre
  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: mapContainerRef.current,
      style: {
        version: 8,
        sources: {
          'osm-tiles': {
            type: 'raster',
            tiles: [
              'https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png',
              'https://b.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png',
              'https://c.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png',
            ],
            tileSize: 256,
            attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; OpenStreetMap',
          },
        },
        layers: [
          {
            id: 'osm-layer',
            type: 'raster',
            source: 'osm-tiles',
            minzoom: 0,
            maxzoom: 20,
          },
        ],
      },
      center: [(defaultBBox[0] + defaultBBox[2]) / 2, (defaultBBox[1] + defaultBBox[3]) / 2],
      zoom: 13,
    });

    // Add navigation controls (zoom, pitch, compass)
    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'bottom-right');
    map.addControl(new maplibregl.ScaleControl({ maxWidth: 120, unit: 'metric' }), 'bottom-left');

    map.on('load', async () => {
      map.fitBounds(defaultBBox, { padding: 50, duration: 1500 });

      // Initialize Geoman
      try {
        const gm = new Geoman(map, {
          controls: {
            draw: {
              marker: {},
              circle: {},
              line: {},
              polygon: {},
              rectangle: {},
            },
            edit: {
              change: {},
              drag: {},
              delete: {},
            },
          } as any,
        });
        geomanRef.current = gm;

        // Listen for Geoman events
        (map as any).on('gm:create', (e: any) => {
          const feature = e.feature || e.shape || e;
          if (feature) {
            onFeatureCreated(feature);
          }
        });

        (map as any).on('gm:edit', (e: any) => {
          const feature = e.feature || e.shape || e;
          if (feature) {
            onFeatureUpdated(feature);
          }
        });

        (map as any).on('gm:remove', (e: any) => {
          const feature = e.feature || e.shape || e;
          const id = feature?.id || feature?.properties?.id;
          if (id) {
            onFeatureDeleted(String(id));
          }
        });
      } catch (err) {
        console.error('Failed to init Geoman:', err);
      }
    });

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // 2. FlyTo/FitBounds when defaultBBox changes (e.g. backend switch)
  useEffect(() => {
    if (!mapRef.current) return;
    mapRef.current.fitBounds(defaultBBox, { padding: 60, duration: 1500 });
  }, [defaultBBox]);

  // 3. Render and Update Layers
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !map.isStyleLoaded()) return;

    layers.forEach((layer) => {
      const sourceId = `src-${layer.id}`;
      const fillLayerId = `layer-${layer.id}-fill`;
      const lineLayerId = `layer-${layer.id}-line`;
      const circleLayerId = `layer-${layer.id}-circle`;

      const data = layerData[layer.id];
      const isVisible = layerVisibility[layer.id] ?? true;
      const opacity = layerOpacity[layer.id] ?? 0.8;

      if (!data) return;

      // Add or update source
      const existingSource = map.getSource(sourceId) as maplibregl.GeoJSONSource;
      if (!existingSource) {
        map.addSource(sourceId, {
          type: 'geojson',
          data: data,
        });
      } else {
        existingSource.setData(data);
      }

      // Add layers if they don't exist
      // Polygon Fill
      if (!map.getLayer(fillLayerId)) {
        map.addLayer({
          id: fillLayerId,
          type: 'fill',
          source: sourceId,
          filter: ['in', ['geometry-type'], ['literal', ['Polygon', 'MultiPolygon']]],
          paint: {
            'fill-color': layer.color,
            'fill-opacity': opacity * 0.5,
          },
        });

        // Click popup handler
        map.on('click', fillLayerId, (e) => {
          if (!e.features || e.features.length === 0) return;
          const feat = e.features[0];
          showPopup(map, e.lngLat, feat, layer.name);
        });

        map.on('mouseenter', fillLayerId, () => {
          map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', fillLayerId, () => {
          map.getCanvas().style.cursor = '';
        });
      } else {
        map.setPaintProperty(fillLayerId, 'fill-opacity', opacity * 0.5);
        map.setLayoutProperty(fillLayerId, 'visibility', isVisible ? 'visible' : 'none');
      }

      // Line / Border Stroke
      if (!map.getLayer(lineLayerId)) {
        map.addLayer({
          id: lineLayerId,
          type: 'line',
          source: sourceId,
          paint: {
            'line-color': layer.color,
            'line-width': layer.id === 'boundary' ? 3 : 1.5,
            'line-opacity': opacity,
          },
        });
      } else {
        map.setPaintProperty(lineLayerId, 'line-opacity', opacity);
        map.setLayoutProperty(lineLayerId, 'visibility', isVisible ? 'visible' : 'none');
      }

      // Point / Circle
      if (!map.getLayer(circleLayerId)) {
        map.addLayer({
          id: circleLayerId,
          type: 'circle',
          source: sourceId,
          filter: ['in', ['geometry-type'], ['literal', ['Point', 'MultiPoint']]],
          paint: {
            'circle-color': layer.color,
            'circle-radius': 6,
            'circle-stroke-width': 2,
            'circle-stroke-color': '#ffffff',
            'circle-opacity': opacity,
          },
        });

        map.on('click', circleLayerId, (e) => {
          if (!e.features || e.features.length === 0) return;
          const feat = e.features[0];
          showPopup(map, e.lngLat, feat, layer.name);
        });

        map.on('mouseenter', circleLayerId, () => {
          map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', circleLayerId, () => {
          map.getCanvas().style.cursor = '';
        });
      } else {
        map.setPaintProperty(circleLayerId, 'circle-opacity', opacity);
        map.setLayoutProperty(circleLayerId, 'visibility', isVisible ? 'visible' : 'none');
      }
    });
  }, [layers, layerData, layerVisibility, layerOpacity]);

  // Helper function to show rich attribute popup
  const showPopup = (map: maplibregl.Map, lngLat: maplibregl.LngLat, feat: any, layerName: string) => {
    if (popupRef.current) {
      popupRef.current.remove();
    }

    const props = feat.properties || {};
    const entries = Object.entries(props).filter(([k]) => !k.startsWith('_'));

    const rowsHtml = entries
      .slice(0, 10)
      .map(
        ([k, v]) => `
        <tr class="border-b border-slate-700/50">
          <td class="py-1 px-1.5 font-medium text-slate-400 font-mono text-[11px]">${k}</td>
          <td class="py-1 px-1.5 text-slate-100 font-semibold text-[11px]">${String(v ?? '-')}</td>
        </tr>
      `
      )
      .join('');

    const popupHtml = `
      <div class="max-w-[280px]">
        <div class="flex items-center justify-between pb-1.5 mb-1.5 border-b border-slate-700">
          <h4 class="text-xs font-bold text-blue-400 truncate">${layerName}</h4>
          <span class="text-[10px] text-slate-400 font-mono px-1 py-0.5 rounded bg-slate-800">
            ${feat.geometry?.type || 'Geometry'}
          </span>
        </div>
        <div class="max-h-48 overflow-y-auto">
          <table class="w-full text-left">
            <tbody>${rowsHtml || '<tr><td class="text-slate-500 py-1 text-xs">No attributes</td></tr>'}</tbody>
          </table>
        </div>
      </div>
    `;

    popupRef.current = new maplibregl.Popup({ closeButton: true, maxWidth: '320px' })
      .setLngLat(lngLat)
      .setHTML(popupHtml)
      .addTo(map);
  };

  return (
    <div className="relative flex-1 h-full w-full">
      <div ref={mapContainerRef} className="absolute inset-0 w-full h-full" />
    </div>
  );
};
