import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

type LatLon = [number, number];
export type MapProps = {
  durationInFrames?: number; fps?: number;
  map: {src: string; z: number; x0: number; y0: number; w: number; h: number};
  camera: {f: number; center: LatLon; width: number}[];          // width = số px ảnh bản đồ hiện vừa khung ngang 1080
  routes: {coords: [number, number][]; color: string; width?: number; from: number; to: number; dash?: boolean; glow?: boolean}[];
  markers: {at: LatLon; label: string; sub?: string; color: string; f: number; side?: 'left' | 'right'; pulse?: boolean; ly?: number}[];
  chips?: {at: LatLon; text: string; color: string; f: number; dx?: number; dy?: number}[];
  attribution?: string;
};

const proj = (m: MapProps['map'], [lat, lon]: LatLon) => {
  const n = 2 ** m.z * 256, r = (lat * Math.PI) / 180;
  const x = ((lon + 180) / 360) * n - m.x0 * 256;
  const y = ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * n - m.y0 * 256;
  return [x, y];
};

export const MapRoute: React.FC<MapProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  // camera: nội suy giữa các mốc
  const cams = p.camera;
  let i = 0; while (i < cams.length - 1 && frame >= cams[i + 1].f) i++;
  const a = cams[i], b = cams[Math.min(i + 1, cams.length - 1)];
  const t = b.f === a.f ? 0 : interpolate(frame, [a.f, b.f], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const lat = a.center[0] + (b.center[0] - a.center[0]) * t, lon = a.center[1] + (b.center[1] - a.center[1]) * t;
  const camW = a.width + (b.width - a.width) * t;
  const s = W / camW;
  const [cx, cy] = proj(p.map, [lat, lon]);
  const tx = W / 2 - cx * s, ty = H / 2 - cy * s;
  const toScreen = (ll: LatLon) => { const [x, y] = proj(p.map, ll); return [x * s + tx, y * s + ty]; };

  return (
    <AbsoluteFill style={{background: '#0b1220', fontFamily: 'Inter, "Noto Sans", sans-serif', overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: p.map.w, height: p.map.h, transformOrigin: '0 0', transform: `translate(${tx}px,${ty}px) scale(${s})`}}>
        <Img src={staticFile(p.map.src)} style={{width: p.map.w, height: p.map.h, filter: 'invert(1) hue-rotate(180deg) brightness(0.95) contrast(0.9) saturate(0.55)'}} />
      </div>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(11,18,32,0) 35%, rgba(11,18,32,.75) 100%)'}} />
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter></defs>
        {p.routes.map((r, k) => {
          const prog = interpolate(frame, [r.from, r.to], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.quad)});
          if (prog <= 0) return null;
          const d = r.coords.map(([lo, la], j) => { const [x, y] = toScreen([la, lo]); return `${j ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`; }).join(' ');
          return <g key={k} filter={r.glow === false ? undefined : 'url(#glow)'}>
            <path d={d} pathLength={1} fill="none" stroke={r.color} strokeWidth={r.width ?? 12} strokeLinecap="round" strokeLinejoin="round"
              strokeDasharray={r.dash ? undefined : '1 1'} strokeDashoffset={r.dash ? undefined : 1 - prog} opacity={r.dash ? prog : 1}
              style={r.dash ? {strokeDasharray: '0.012 0.01'} : undefined} />
          </g>;
        })}
      </svg>
      {p.markers.map((m, k) => {
        const sp = spring({frame: frame - m.f, fps, config: {damping: 12}});
        if (frame < m.f) return null;
        const [x, y] = toScreen(m.at);
        const pulse = m.pulse ? 1 + 0.25 * Math.sin((frame - m.f) / 5) : 1;
        const right = m.side !== 'left';
        return <div key={k} style={{position: 'absolute', left: x, top: y, transform: `scale(${sp})`}}>
          <div style={{position: 'absolute', left: -22, top: -22, width: 44, height: 44, borderRadius: 22, background: m.color, opacity: .35, transform: `scale(${pulse * 1.6})`}} />
          <div style={{position: 'absolute', left: -14, top: -14, width: 28, height: 28, borderRadius: 14, background: m.color, border: '5px solid #fff', boxShadow: '0 0 18px rgba(0,0,0,.6)'}} />
          <div style={{position: 'absolute', top: -34 + (m.ly ?? 0), ...(right ? {left: 34} : {right: 34}), whiteSpace: 'nowrap', background: 'rgba(11,18,32,.88)', border: `3px solid ${m.color}`, borderRadius: 14, padding: '8px 18px', color: '#fff'}}>
            <div style={{fontSize: 38, fontWeight: 800, lineHeight: 1.1}}>{m.label}</div>
            {m.sub && <div style={{fontSize: 26, fontWeight: 600, opacity: .85}}>{m.sub}</div>}
          </div>
        </div>;
      })}
      {(p.chips || []).map((c, k) => {
        if (frame < c.f) return null;
        const sp = spring({frame: frame - c.f, fps, config: {damping: 14}});
        const [x, y] = toScreen(c.at);
        const cxs = Math.min(Math.max(x + (c.dx ?? 0), 300), W - 300);
        return <div key={k} style={{position: 'absolute', left: cxs, top: y + (c.dy ?? 0), transform: `translate(-50%,-50%) scale(${sp})`, whiteSpace: 'nowrap',
          background: c.color, color: '#0b1220', fontSize: 34, fontWeight: 800, borderRadius: 999, padding: '10px 26px', boxShadow: '0 8px 24px rgba(0,0,0,.5)'}}>{c.text}</div>;
      })}
      <div style={{position: 'absolute', left: 110, top: 1240, color: 'rgba(255,255,255,.6)', fontSize: 20}}>{p.attribution ?? '© OpenStreetMap contributors'}</div>
    </AbsoluteFill>
  );
};
