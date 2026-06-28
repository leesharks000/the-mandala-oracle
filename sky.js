// sky.js — the actual night sky.
//
// v1.2 (2026-06-29) — switched from custom ShaderMaterial to built-in
// PointsMaterial in magnitude buckets. The custom shader was failing
// silently on mobile WebGL, throwing inside buildStars() and preventing
// animate() from ever starting — so the entire scene was invisible.
//
// PointsMaterial is three.js's vanilla path: precision qualifiers handled
// by the library, no shader compilation we can break. We sacrifice the
// per-point continuously-varying size (custom shader) for a 7-bucket
// approximation by apparent magnitude. Visually equivalent on a sky where
// stars are quantized into Hipparcos magnitudes anyway.
//
// Other resilience improvements:
//   • animate() starts unconditionally — if star-building throws, the
//     scene still renders (camera, controls, whatever DID succeed)
//   • each setup step in its own try/catch with explicit log
//   • larger point sizes (sky doesn't need parallax — sizeAttenuation:false
//     and bigger pixel sizes so points are actually visible on mobile)

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ─────────────────────────────────────────────────────────────────────────
// Observer + constants
// ─────────────────────────────────────────────────────────────────────────

const DEFAULT_OBSERVER = { lat: 42.33, lng: -83.05, name: 'Detroit' };
const OBSERVER = window.skyObserver || DEFAULT_OBSERVER;

const SKY_RADIUS = 800;

// Magnitude buckets — each bucket gets its own Points object with its own
// PointsMaterial. Pixel sizes generous because mobile high-DPI eats them.
const MAG_BUCKETS = [
  { max_mag: 0.5, size: 18 },  // Sirius, Canopus, Arcturus, Vega
  { max_mag: 1.5, size: 12 },  // bright stars: Betelgeuse, Rigel, Procyon
  { max_mag: 2.5, size: 8  },  // Big Dipper bowl, Polaris
  { max_mag: 3.5, size: 5  },
  { max_mag: 4.5, size: 3.5 },
  { max_mag: 5.5, size: 2.5 },
  { max_mag: 6.5, size: 1.8 },
];

// ─────────────────────────────────────────────────────────────────────────
// Local sidereal time — Meeus Astronomical Algorithms ch. 12
// ─────────────────────────────────────────────────────────────────────────

function julianDate(date) {
  return date.getTime() / 86400000 + 2440587.5;
}

function localSiderealTimeHours(date, longitudeDeg) {
  const jd = julianDate(date);
  const T = (jd - 2451545.0) / 36525;
  let gmstDeg = 280.46061837
              + 360.98564736629 * (jd - 2451545.0)
              + 0.000387933 * T * T
              - (T * T * T) / 38710000;
  gmstDeg = ((gmstDeg % 360) + 360) % 360;
  const lstDeg = ((gmstDeg + longitudeDeg) % 360 + 360) % 360;
  return lstDeg / 15;
}

// ─────────────────────────────────────────────────────────────────────────
// Scene setup
// ─────────────────────────────────────────────────────────────────────────

const canvas = document.getElementById('sky-canvas');
const container = document.getElementById('sky-canvas-container');

console.log('[sky] container size:', container?.clientWidth, 'x', container?.clientHeight);

const scene = new THREE.Scene();
scene.background = null;

const camera = new THREE.PerspectiveCamera(
  60, container.clientWidth / container.clientHeight, 0.1, 5000
);
camera.position.set(0, 0, 0.5);
camera.lookAt(0, 0, -1);

let renderer;
try {
  renderer = new THREE.WebGLRenderer({
    canvas, antialias: true, alpha: true,
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(container.clientWidth, container.clientHeight);
  console.log('[sky] WebGL renderer created, pixelRatio:', renderer.getPixelRatio());
} catch (e) {
  console.error('[sky] WebGL renderer creation failed:', e);
}

const controls = renderer ? new OrbitControls(camera, canvas) : null;
if (controls) {
  controls.target.set(0, 0, 0);
  controls.enableZoom = false;
  controls.enablePan = false;
  controls.enabled = false;
  controls.rotateSpeed = 0.25;
  controls.minPolarAngle = Math.PI * 0.10;
  controls.maxPolarAngle = Math.PI * 0.50;
}

const celestialSphere = new THREE.Group();
scene.add(celestialSphere);

// ─────────────────────────────────────────────────────────────────────────
// Coordinate transforms
// ─────────────────────────────────────────────────────────────────────────

function equatorialToCartesian(raHours, decDeg, radius = SKY_RADIUS) {
  const ra = raHours * 15 * Math.PI / 180;
  const dec = decDeg * Math.PI / 180;
  return {
    x: -radius * Math.cos(dec) * Math.sin(ra),
    y: radius * Math.sin(dec),
    z: -radius * Math.cos(dec) * Math.cos(ra),
  };
}

function applyCelestialAlignment(date) {
  const lstHours = localSiderealTimeHours(date, OBSERVER.lng);
  const lstRad = lstHours * 15 * Math.PI / 180;
  const latRad = OBSERVER.lat * Math.PI / 180;
  celestialSphere.rotation.set(0, 0, 0);
  celestialSphere.rotateOnWorldAxis(new THREE.Vector3(0, 1, 0), -lstRad);
  celestialSphere.rotateOnWorldAxis(new THREE.Vector3(1, 0, 0), Math.PI / 2 - latRad);
}

// ─────────────────────────────────────────────────────────────────────────
// Star color from B-V
// ─────────────────────────────────────────────────────────────────────────

function ciToColor(ci) {
  let r, g, b;
  if (ci < -0.3)      { r = 0.65; g = 0.75; b = 1.0;  }
  else if (ci < 0.0)  { r = 0.80; g = 0.88; b = 1.0;  }
  else if (ci < 0.3)  { r = 1.0;  g = 0.98; b = 0.95; }
  else if (ci < 0.6)  { r = 1.0;  g = 0.95; b = 0.78; }
  else if (ci < 1.0)  { r = 1.0;  g = 0.86; b = 0.62; }
  else if (ci < 1.5)  { r = 1.0;  g = 0.74; b = 0.45; }
  else                { r = 1.0;  g = 0.55; b = 0.38; }
  return new THREE.Color(r, g, b);
}

// ─────────────────────────────────────────────────────────────────────────
// Star texture (soft glow)
// ─────────────────────────────────────────────────────────────────────────

function makeStarTexture() {
  const size = 64;
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  grad.addColorStop(0.0,  'rgba(255,255,255,1)');
  grad.addColorStop(0.25, 'rgba(255,255,255,0.7)');
  grad.addColorStop(0.5,  'rgba(255,255,255,0.25)');
  grad.addColorStop(1.0,  'rgba(255,255,255,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(c);
  tex.needsUpdate = true;
  return tex;
}
const starTexture = makeStarTexture();

// ─────────────────────────────────────────────────────────────────────────
// Build stars — one Points object per magnitude bucket, using
// PointsMaterial (built-in, robust). Stars below the brightest cutoff
// for a bucket but at-or-above the next-brighter bucket's cutoff go in.
// ─────────────────────────────────────────────────────────────────────────

function buildStars(stars) {
  let totalBuilt = 0;
  let prevMagCutoff = -Infinity;

  for (const bucket of MAG_BUCKETS) {
    const inBucket = stars.filter(s => s.mag >= prevMagCutoff && s.mag < bucket.max_mag);
    prevMagCutoff = bucket.max_mag;
    if (inBucket.length === 0) continue;

    const positions = [];
    const colors = [];
    for (const star of inBucket) {
      const pos = equatorialToCartesian(star.ra, star.dec);
      positions.push(pos.x, pos.y, pos.z);
      const c = ciToColor(star.ci || 0);
      colors.push(c.r, c.g, c.b);
    }

    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geom.setAttribute('color',    new THREE.Float32BufferAttribute(colors, 3));

    const mat = new THREE.PointsMaterial({
      size: bucket.size,
      sizeAttenuation: false,    // absolute pixel sizes; sky has no parallax
      map: starTexture,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      vertexColors: true,
    });

    const points = new THREE.Points(geom, mat);
    celestialSphere.add(points);
    totalBuilt += inBucket.length;
    console.log(`[sky] bucket mag<${bucket.max_mag}: ${inBucket.length} stars at ${bucket.size}px`);
  }

  console.log(`[sky] built ${totalBuilt} stars total`);
}

// ─────────────────────────────────────────────────────────────────────────
// Label sprites
// ─────────────────────────────────────────────────────────────────────────

function makeLabelSprite(text, color = '#d8c8a8', scale = 0.6) {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 128;
  const ctx = c.getContext('2d');
  ctx.font = 'italic 30px Georgia, "EB Garamond", serif';
  ctx.fillStyle = color;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.shadowColor = 'rgba(0,0,0,0.95)';
  ctx.shadowBlur = 12;
  ctx.fillText(text, 256, 64);
  const tex = new THREE.CanvasTexture(c);
  tex.needsUpdate = true;
  const mat = new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.9 });
  const sprite = new THREE.Sprite(mat);
  sprite.scale.set(80 * scale, 20 * scale, 1);
  return sprite;
}

function buildZodiacLabels(zodiac) {
  for (const sign of zodiac.zodiac) {
    const top = equatorialToCartesian(sign.ra_center_hours, sign.dec_center_degrees, SKY_RADIUS * 0.95);
    const label = makeLabelSprite(`${sign.symbol} ${sign.sign}`, '#d8c8a8', 0.9);
    label.position.set(top.x, top.y, top.z);
    celestialSphere.add(label);

    const below = equatorialToCartesian(sign.ra_center_hours, sign.dec_center_degrees - 4, SKY_RADIUS * 0.95);
    const hetLabel = makeLabelSprite(sign.heteronym, '#a89878', 0.6);
    hetLabel.position.set(below.x, below.y, below.z);
    celestialSphere.add(hetLabel);
  }
  console.log(`[sky] built ${zodiac.zodiac.length} zodiacal regions`);
}

function buildCanonicalLabels(zodiac, stars) {
  const byName = new Map();
  for (const s of stars) if (s.name) byName.set(s.name.toLowerCase(), s);
  let count = 0;
  for (const ct of zodiac.canonical_text_stars) {
    const starName = ct.anchor_to_star.split(' ')[0].toLowerCase();
    const star = byName.get(starName);
    if (!star) { console.warn(`[sky] anchor star not found for "${ct.title}": ${ct.anchor_to_star}`); continue; }
    const pos = equatorialToCartesian(star.ra, star.dec - 2, SKY_RADIUS * 0.93);
    const label = makeLabelSprite(ct.title, '#e8d8a8', 0.65);
    label.position.set(pos.x, pos.y, pos.z);
    celestialSphere.add(label);
    count++;
  }
  console.log(`[sky] built ${count} canonical text labels`);
}

// ─────────────────────────────────────────────────────────────────────────
// Modes
// ─────────────────────────────────────────────────────────────────────────

function setMode(mode) {
  if (controls) controls.enabled = (mode === 'merkabah');
}

// ─────────────────────────────────────────────────────────────────────────
// Resize + Animate (starts unconditionally)
// ─────────────────────────────────────────────────────────────────────────

function onResize() {
  if (!renderer) return;
  const w = container.clientWidth;
  const h = container.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
}
window.addEventListener('resize', onResize);

let animateStarted = false;
function startAnimate() {
  if (animateStarted || !renderer) return;
  animateStarted = true;
  function frame() {
    requestAnimationFrame(frame);
    applyCelestialAlignment(new Date());
    if (controls) controls.update();
    renderer.render(scene, camera);
  }
  frame();
  console.log('[sky] animate loop started');
}

// ─────────────────────────────────────────────────────────────────────────
// Boot — each step independently fault-tolerant
// ─────────────────────────────────────────────────────────────────────────

async function boot() {
  console.log(`[sky] booting v1.2 — observer ${OBSERVER.name} (${OBSERVER.lat}, ${OBSERVER.lng})`);

  // Start the render loop FIRST so anything that does succeed is visible.
  startAnimate();

  let stars = null, zodiac = null;
  try {
    const r = await fetch('/sky/stars.json');
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    stars = await r.json();
    console.log(`[sky] fetched stars.json: ${stars.length} stars`);
  } catch (e) { console.error('[sky] stars.json fetch failed:', e); }

  try {
    const r = await fetch('/sky/zodiac.json');
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    zodiac = await r.json();
    console.log(`[sky] fetched zodiac.json`);
  } catch (e) { console.error('[sky] zodiac.json fetch failed:', e); }

  if (stars) {
    try { buildStars(stars); } catch (e) { console.error('[sky] buildStars failed:', e); }
  }
  if (zodiac) {
    try { buildZodiacLabels(zodiac); } catch (e) { console.error('[sky] buildZodiacLabels failed:', e); }
  }
  if (zodiac && stars) {
    try { buildCanonicalLabels(zodiac, stars); } catch (e) { console.error('[sky] buildCanonicalLabels failed:', e); }
  }

  window.sky = { setMode, observer: OBSERVER };
  window.dispatchEvent(new CustomEvent('sky-ready', {
    detail: { starCount: stars ? stars.length : 0, observer: OBSERVER },
  }));

  console.log('[sky] booted');
}

boot();
