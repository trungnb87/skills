"""Dựng cảnh bản đồ động (mp4 1080x1920) bằng Remotion từ một file mô tả JSON.

    python3 make_map.py ban-do.json

Mô tả (thời gian tính bằng giây, tọa độ [vĩ độ, kinh độ]):
{
  "out": "broll/bando.mp4", "seconds": 7.7,
  "points": {"pho_co": [21.0188, 105.8630], "thu_lam": [21.1372, 105.9105]},
  "routes": [   // "road": đi theo đường thật (OSRM); "line": nối thẳng các điểm (cầu đang xây, tuyến dự kiến)
    {"road": ["pho_co", "thu_lam"], "color": "#e2e8f0", "start": 0.6, "end": 3.2},
    {"line": ["thu_lam", [21.07, 105.85]], "color": "#f5c542", "start": 4.0, "end": 6.4}
  ],
  "markers": [{"at": "pho_co", "label": "Phố cổ", "sub": "phường Hồng Hà", "color": "#e2e8f0", "t": 0.1, "side": "right"}],
  "chips": [{"at": "thu_lam", "text": "~20 km", "color": "#e2e8f0", "t": 2.7, "dx": 0, "dy": 0}],
  "camera": [{"t": 0, "fit": ["pho_co", "thu_lam"], "zoom": 1.15}, {"t": 5, "fit": ["pho_co", "thu_lam", "tay_ho"]}]
}
Nền bản đồ: OpenStreetMap (ghi "© OpenStreetMap contributors" trên hình). Lần đầu chạy tự cài Remotion vào thư mục này.
"""
import json, math, os, subprocess, sys, urllib.request, shutil, glob

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
BOX = (90, 330, 990, 1430)   # vùng an toàn để đặt bản đồ: tránh header TikTok phía trên và phụ đề phía dưới

def chrome():
    for p in glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome') + glob.glob(os.path.expanduser('~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome')) + ['/usr/bin/google-chrome', '/usr/bin/chromium']:
        if os.path.exists(p): return p
    return None

def osrm(pts):
    s = ';'.join(f'{lo},{la}' for la, lo in pts)
    u = f'https://router.project-osrm.org/route/v1/driving/{s}?overview=full&geometries=geojson'
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'diem-bao-video'}), timeout=30))['routes'][0]
    print(f'  đường {round(r["distance"]/1000, 1)} km, ô tô ~{round(r["duration"]/60)} phút')
    return r['geometry']['coordinates']

def main(path):
    spec = json.load(open(path)); base = os.path.dirname(os.path.abspath(path))
    P = {k: v for k, v in spec['points'].items()}
    pt = lambda x: P[x] if isinstance(x, str) else x
    allp = [pt(x) for x in P]
    routes = []
    for r in spec['routes']:
        if 'road' in r: coords = osrm([pt(x) for x in r['road']])
        else: coords = [[pt(x)[1], pt(x)[0]] for x in r['line']]
        allp += [[c[1], c[0]] for c in coords]
        coords = coords[::max(1, len(coords) // 300)] + [coords[-1]]
        routes.append({'coords': coords, 'color': r.get('color', '#f5c542'), 'width': r.get('width', 13), 'from': round(r['start'] * FPS), 'to': round(r['end'] * FPS), 'dash': r.get('dash', False)})
    lats = [p[0] for p in allp]; lons = [p[1] for p in allp]
    pad = 0.35
    la0, la1 = min(lats) - (max(lats) - min(lats)) * pad - 0.01, max(lats) + (max(lats) - min(lats)) * pad + 0.01
    lo0, lo1 = min(lons) - (max(lons) - min(lons)) * pad - 0.03, max(lons) + (max(lons) - min(lons)) * pad + 0.03
    span = max(la1 - la0, lo1 - lo0)
    z = 15 if span < 0.12 else 14 if span < 0.3 else 13 if span < 0.6 else 12 if span < 1.2 else 10
    pub = os.path.join(HERE, 'public'); os.makedirs(pub, exist_ok=True)
    subprocess.run([sys.executable, os.path.join(HERE, 'tiles.py'), str(la0), str(lo0), str(la1), str(lo1), str(z), pub], check=True)
    M = json.load(open(os.path.join(pub, 'map.json')))
    def proj(lat, lon):
        n = 2 ** M['z'] * 256; r = math.radians(lat)
        return ((lon + 180) / 360 * n - M['x0'] * 256, (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * n - M['y0'] * 256)
    def unproj(x, y):
        n = 2 ** M['z'] * 256; lon = (x + M['x0'] * 256) / n * 360 - 180
        yy = (y + M['y0'] * 256) / n; return [math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * yy)))), lon]
    def fit(names, zoom=1.0):
        ps = [pt(x) for x in names]; xs, ys = zip(*[proj(*p) for p in ps])
        s = min((BOX[2] - BOX[0]) / max(max(xs) - min(xs), 1), (BOX[3] - BOX[1]) / max(max(ys) - min(ys), 1)) * zoom
        bx, by = (BOX[0] + BOX[2]) / 2 - 540, (BOX[1] + BOX[3]) / 2 - 960
        return unproj((min(xs) + max(xs)) / 2 - bx / s, (min(ys) + max(ys)) / 2 - by / s), 1080 / s
    cams = []
    for c in spec.get('camera', [{'t': 0, 'fit': list(P)}]):
        center, w = fit(c['fit'], c.get('zoom', 1.0)); cams.append({'f': round(c['t'] * FPS), 'center': center, 'width': w})
    props = {'durationInFrames': round(spec['seconds'] * FPS), 'fps': FPS, 'map': {'src': 'map.png', **M}, 'camera': cams, 'routes': routes,
             'markers': [{**{k: v for k, v in m.items() if k not in ('t', 'at')}, 'at': pt(m['at']), 'f': round(m['t'] * FPS)} for m in spec.get('markers', [])],
             'chips': [{**{k: v for k, v in c.items() if k not in ('t', 'at')}, 'at': pt(c['at']), 'f': round(c['t'] * FPS)} for c in spec.get('chips', [])],
             'attribution': '© OpenStreetMap contributors'}
    pj = os.path.join(HERE, 'public', 'props.json'); json.dump(props, open(pj, 'w'), ensure_ascii=False)
    if not os.path.exists(os.path.join(HERE, 'node_modules', 'remotion')):
        subprocess.run(['npm', 'install', '--silent', '--no-audit', '--no-fund'], cwd=HERE, check=True)
    out = os.path.join(base, spec['out']); os.makedirs(os.path.dirname(out), exist_ok=True)
    cmd = ['npx', 'remotion', 'render', 'src/index.ts', 'MapRoute', out, f'--props={pj}', '--codec=h264', '--crf=18']
    if chrome(): cmd.append(f'--browser-executable={chrome()}')
    if '--still' in sys.argv:
        t = float(sys.argv[sys.argv.index('--still') + 1]); out = out.replace('.mp4', f'_{t}.png')
        cmd = ['npx', 'remotion', 'still', 'src/index.ts', 'MapRoute', out, f'--frame={round(t * FPS)}', f'--props={pj}'] + cmd[-1:]
    subprocess.run(cmd, cwd=HERE, check=True); print('Đã xuất', out)

if __name__ == '__main__':
    main(sys.argv[1])
