import React, { useState } from 'react';
import { BookOpen, Code2, Sparkles, ChevronRight } from 'lucide-react';

interface Lesson {
  id: string;
  step: number;
  title: string;
  badge: string;
  summary: string;
  explanation: string;
  codeSnippets: {
    react: string;
    python: string;
    rust: string;
  };
  exercisePrompt: string;
}

const LESSONS_DATA: Lesson[] = [
  {
    id: 'lesson01',
    step: 1,
    title: 'Map Initialization & WGS84 GeoJSON',
    badge: 'Basemap & RFC 7946',
    summary: 'เริ่มต้นสร้าง MapLibre GL instance, ทำความเข้าใจพิกัด WGS84 และลำดับ [Longitude, Latitude]',
    explanation:
      'ในงาน Web GIS แผนที่ MapLibre ทำงานบนระบบพิกัด EPSG:4326 (WGS84) โดยมาตรฐาน GeoJSON (RFC 7946) จะเก็บพิกัดในรูป [Lng, Lat] เสมอ (ต่างจากคำพูดคนทั่วไปที่มักพูด Lat-Long)',
    codeSnippets: {
      react: `// React + MapLibre GL JS
const map = new maplibregl.Map({
  container: 'map-container',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [100.059, 6.616], // [Lng, Lat]
  zoom: 14
});`,
      python: `# Python: สร้าง GeoJSON Point Feature
def create_point(lng: float, lat: float, name: str):
    return {
        "type": "Feature",
        "geometry": { "type": "Point", "coordinates": [lng, lat] },
        "properties": { "name": name }
    }`,
      rust: `// Rust: สร้าง Point Feature ด้วย Serde JSON
pub fn create_point(lng: f64, lat: f64, name: &str) -> Value {
    json!({
        "type": "Feature",
        "geometry": { "type": "Point", "coordinates": [lng, lat] },
        "properties": { "name": name }
    })
}`,
    },
    exercisePrompt: 'ทดสอบสร้าง Point Feature และตรวจเช็คช่วงพิกัด (-180..180, -90..90)',
  },
  {
    id: 'lesson02',
    step: 2,
    title: 'Layer Extraction (Shapefile vs GeoJSON)',
    badge: 'Shapefile & Large GeoJSON',
    summary: 'การแปลง Shapefile (.zip) ใน Python FastAPI และการอ่านไฟล์ GeoJSON ขนาดใหญ่ (LTAX 3,600+ แปลง) ใน Rust',
    explanation:
      'ฝั่ง Python จะใช้ PyShp คลายไฟล์ .zip และอ่านทั้ง .shp (Geometry) และ .dbf (Attributes) พร้อมแปลงรหัสภาษาไทย ส่วนฝั่ง Rust จะใช้ความเร็วของ Serde Deserialization ในการเสิร์ฟ LTAX แปลงที่ดินนับพันแปลงได้แบบเสี้ยววินาที',
    codeSnippets: {
      react: `// MapLibre: เพิ่ม Source และ Layer
map.addSource('parcels', { type: 'geojson', data: geojsonData });
map.addLayer({
  id: 'parcels-fill',
  type: 'fill',
  source: 'parcels',
  paint: { 'fill-color': '#2563eb', 'fill-opacity': 0.4 }
});`,
      python: `# FastAPI: อ่าน Shapefile จาก zip
import shapefile
sf = shapefile.Reader('data/dpt/shapefile/extracted/be_parcel/be_parcel')
for shape_rec in sf.shapeRecords():
    geom = shape_rec.shape.__geo_interface__
    props = shape_rec.record.as_dict()`,
      rust: `// Rust Axum: อ่าน GeoJSON ขนาดใหญ่
pub fn read_ltax_layer(layer_id: &str) -> Option<Value> {
    let path = format!("../data/ltax/geojson/{}.geojson", layer_id);
    let content = fs::read_to_string(path).ok()?;
    serde_json::from_str(&content).ok()
}`,
    },
    exercisePrompt: 'ทดสอบแยกประเภทเรขาคณิต (Polygon / MultiPolygon) และเสิร์ฟผ่าน REST API',
  },
  {
    id: 'lesson03',
    step: 3,
    title: 'Layer Controls & Interactive Popups',
    badge: 'Properties & Popups',
    summary: 'การเปิด/ปิดเลเยอร์, ปรับ Opacity และคลิกเพื่อดึง Attributes (ชื่อเจ้าของ, เลขแปลง) มาแสดงใน Popup',
    explanation:
      'เมื่อผู้ใช้คลิกบนแผนที่ MapLibre จะตรวจสอบว่าคลิกโดน Feature ใดใน Layer แล้วส่ง event.features ออกมา ทำให้เราสามารถอ่าน properties เช่น รหัสแปลงที่ดิน หรือชื่อเจ้าของมาสร้าง HTML Popup สวยงามได้ทันที',
    codeSnippets: {
      react: `// Event คลิก Feature แสดง Popup
map.on('click', 'layer-be_parcel-fill', (e) => {
  const feat = e.features[0];
  const props = feat.properties;
  new maplibregl.Popup()
    .setLngLat(e.lngLat)
    .setHTML(\`<b>แปลง:</b> \${props.name || props.id}\`)
    .addTo(map);
});`,
      python: `# Python: กรองแปลงที่ดินตามชื่อเจ้าของ
def filter_by_owner(features, owner_name):
    return [f for f in features if owner_name in f["properties"].get("owner", "")]`,
      rust: `// Rust: กรอง Properties อย่างรวดเร็ว
pub fn filter_by_property(features: &[Value], key: &str, val: &str) -> Vec<Value> {
    features.iter().filter(|f| f["properties"][key] == val).cloned().collect()
}`,
    },
    exercisePrompt: 'ทดสอบเชื่อมโยง Popup คลิกแสดงข้อมูลแปลงที่ดินจริงบนแผนที่',
  },
  {
    id: 'lesson04',
    step: 4,
    title: 'Spatial Bounding Box & Auto-FitBounds',
    badge: 'BBox & fitBounds',
    summary: 'การคำนวณ BBox [minLng, minLat, maxLng, maxLat] เพื่อให้กล้องแผนที่บิน (FlyTo) ไปยังพิกัดข้อมูลอัตโนมัติ',
    explanation:
      'เมื่อผู้ใช้สลับระหว่าง Rust (ขอนแก่น) กับ FastAPI (สตูล) แผนที่ต้องรู้พิกัดขอบเขต (Bounding Box) ล่วงหน้า เพื่อสั่ง map.fitBounds(bbox, { padding: 50 }) ให้มุมมองครอบคลุมข้อมูลทั้งหมดพอดีโดยไม่ต้องเลื่อนหาเอง',
    codeSnippets: {
      react: `// Frontend: Auto-FitBounds ตาม BBox ของ Backend
const bbox = [100.055, 6.613, 100.065, 6.620]; // สตูล
map.fitBounds(bbox, { padding: 60, duration: 1500 });`,
      python: `# Python: คำนวณ BBox จาก PyShp
bbox = [round(b, 6) for b in sf.bbox] # [minX, minY, maxX, maxY]`,
      rust: `// Rust: คำนวณ Bounding Box จากพิกัด
pub fn calculate_bbox(coords: &[[f64; 2]]) -> [f64; 4] {
    let (mut min_x, mut min_y, mut max_x, mut max_y) = (180.0, 90.0, -180.0, -90.0);
    // iterate and update
    [min_x, min_y, max_x, max_y]
}`,
    },
    exercisePrompt: 'ทดสอบคำนวณ Bounding Box และคำนวณระยะทาง Haversine ระหว่างจุด',
  },
  {
    id: 'lesson05',
    step: 5,
    title: 'Geoman Toolbar & Backend CRUD Persistence',
    badge: 'Geoman + REST CRUD',
    summary: 'ติดตั้ง @geoman-io/maplibre-geoman-free วาดรูปทรง, แก้ไขจุดพิกัด (Vertices), ลบ และบันทึกลง API',
    explanation:
      'Geoman ให้เครื่องมือวาด Point, Line, Polygon, Rectangle พร้อมโหมดแก้ไขจุดยอด (Edit Vertices) และโหมดลบ (Delete) เมื่อผู้ใช้ทำงานเสร็จ จะเกิด Event เช่น gm:create หรือ gm:edit ซึ่งเราจะส่งคำขอ POST / PUT / DELETE ไปยัง Backend เพื่อบันทึกลง user_drawings.geojson ทันที',
    codeSnippets: {
      react: `// Geoman Setup & Event Binding
const gm = new Geoman(map, {
  controls: { draw: { polygon: true, marker: true }, edit: { change: true, delete: true } }
});

map.on('gm:create', (e) => {
  api.createFeature(e.feature); // Sync to Backend!
});`,
      python: `# FastAPI: บันทึก Feature ที่วาดใหม่
@app.post("/api/features")
def create_feature(feature: dict):
    return shapefile_service.add_user_feature(feature)`,
      rust: `// Rust Axum: บันทึก Feature ที่วาดใหม่
pub async fn create_feature(Json(payload): Json<Value>) -> impl IntoResponse {
    storage_service::add_user_feature(payload)
}`,
    },
    exercisePrompt: 'ทดสอบวาดโพลิกอนบนแผนที่ แล้วกด Reset Drawings เพื่อคืนค่า',
  },
];

export const LearningSidebar: React.FC = () => {
  const [selectedLessonIndex, setSelectedLessonIndex] = useState(0);
  const [codeLanguage, setCodeLanguage] = useState<'react' | 'python' | 'rust'>('python');

  const currentLesson = LESSONS_DATA[selectedLessonIndex];

  return (
    <div className="w-96 bg-slate-900 border-l border-slate-800 flex flex-col h-full z-20 shadow-2xl">
      {/* Header */}
      <div className="p-3 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <BookOpen className="w-4 h-4 text-blue-400" />
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-200">
            หลักสูตร MapLibre & GIS API
          </h2>
        </div>
        <span className="text-[10px] text-blue-400 font-mono px-2 py-0.5 rounded bg-blue-500/10 border border-blue-500/20">
          5 Lessons
        </span>
      </div>

      {/* Lesson Selector Pills */}
      <div className="p-2 border-b border-slate-800 bg-slate-950/50 flex space-x-1 overflow-x-auto">
        {LESSONS_DATA.map((lesson, idx) => (
          <button
            key={lesson.id}
            onClick={() => setSelectedLessonIndex(idx)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition flex items-center gap-1.5 ${
              selectedLessonIndex === idx
                ? 'bg-blue-600 text-white font-semibold shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <span>บทที่ {lesson.step}</span>
            {selectedLessonIndex === idx && <ChevronRight className="w-3 h-3" />}
          </button>
        ))}
      </div>

      {/* Lesson Content Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Title & Badge */}
        <div>
          <div className="flex items-center space-x-2 mb-1">
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
              {currentLesson.badge}
            </span>
            <span className="text-xs text-slate-400 font-medium">Step {currentLesson.step} of 5</span>
          </div>
          <h3 className="text-base font-bold text-white leading-snug">{currentLesson.title}</h3>
          <p className="text-xs text-slate-300 mt-2 leading-relaxed bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/60">
            {currentLesson.summary}
          </p>
        </div>

        {/* Detailed Explanation */}
        <div className="text-xs text-slate-300 space-y-2 leading-relaxed">
          <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wide flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" /> คำอธิบายหลักการทำงาน
          </h4>
          <p>{currentLesson.explanation}</p>
        </div>

        {/* Code Snippet Viewer with Language Tabs */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wide flex items-center gap-1.5">
              <Code2 className="w-3.5 h-3.5 text-blue-400" /> ตัวอย่างโค้ด (Code Comparison)
            </h4>
            <div className="flex bg-slate-950 p-0.5 rounded-lg border border-slate-800 text-[10px]">
              {(['react', 'python', 'rust'] as const).map((lang) => (
                <button
                  key={lang}
                  onClick={() => setCodeLanguage(lang)}
                  className={`px-2 py-0.5 rounded uppercase font-mono transition ${
                    codeLanguage === lang
                      ? 'bg-blue-600 text-white font-bold'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {lang}
                </button>
              ))}
            </div>
          </div>

          <pre className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-emerald-400 font-mono text-[11px] overflow-x-auto leading-relaxed">
            <code>{currentLesson.codeSnippets[codeLanguage]}</code>
          </pre>
        </div>

        {/* Try-it-yourself prompt (no automatic check: the course exercises are checked in the terminal) */}
        <div className="p-3 rounded-xl bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 space-y-2.5">
          <h4 className="text-xs font-bold text-white flex items-center gap-1.5">🎯 ลองทำดู</h4>
          <p className="text-[11px] text-slate-300">{currentLesson.exercisePrompt}</p>
        </div>
      </div>
    </div>
  );
};

