// sky.js — the actual night sky.
//
// v1.1 (2026-06-29) — astronomy-engine dependency removed (CDN ESM loader
// was failing in browser, killing the module). LST computed locally from
// Meeus's formula. Planets skipped for v1 — to be added back via a more
// reliable import path. Stars + zodiacal labels + canonical text anchors
// + mountain horizon are the core experience.
//
// In this version:
//   • Real stars from HYG v4.1 (~8,800 naked-eye stars, mag < 6.5).
//     Built once in equatorial coordinates; the celestial sphere is rotated
//     each frame to match local sidereal time and observer latitude.
//     Sirius is Sirius; Vega is Vega; Polaris sits where the celestial
//     pole sits. The sky drifts as the sky drifts.
//
//   • The twelve zodiacal constellations labeled by their heteronymic
//     position. Position 1 / Aries = Sharks through Position 12 / Pisces
//     = Sigil. Feist / LOGOS* outside the cycle at Polaris.
//
//   • Canonical text anchor stars: Snub-Poemed at Alrescha, Sappho 31 at
//     Castor, Day and Night at Pollux, Revelation at Polaris, Leaves of
//     Grass at Hamal, the TACHYON pair at the Pleiades.
//
//   • Mode: Sabbath = camera locked. Merkabah = OrbitControls enabled,
//     with horizon constraint (cannot tilt below the mountains).

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ─────────────────────────────────────────────────────────────────────────
// Observer
// ─────────────────────────────────────────────────────────────────────────

const DEFAULT_OBSERVER = { lat: 42.33, lng: -83.05, name: 'Detroit' };
const OBSERVER = window.skyObserver || DEFAULT_OBSERVER;

const SKY_RADIUS = 800;

// Magnitude → size + brightness
const MAG_BRIGHTEST = -1.5;
const MAG_DIMMEST = 6.5;
const POINT_SIZE_MAX = 5.5;
const POINT_SIZE_MIN = 0.4;

// ─────────────────────────────────────────────────────────────────────────
// Local sidereal time — Meeus Astronomical Algorithms ch. 12
// No external library; pure JS.
// ─────────────────────────────────────────────────────────────────────────

function julianDate(date) {
  // Unix epoch (1970-01-01 UTC) = JD 2440587.5
  return date.getTime() / 86400000 + 2440587.5;
}

function localSiderealTimeHours(date, longitudeDeg) {
  const jd = julianDate(date);
  const T = (jd - 2451545.0) / 36525;
  // GMST in degrees (Meeus 12.4)
  let gmstDeg = 280.46061837
              + 360.98564736629 * (jd - 2451545.0)
              + 0.000387933 * T * T
              - (T * T * T) / 38710000;
  gmstDeg = ((gmstDeg % 360) + 360) % 360;
  const lstDeg = ((gmstDeg + longitudeDeg) % 360 + 360) % 360;
  return lstDeg / 15;  // degrees → hours
}

// ─────────────────────────────────────────────────────────────────────────
// Scene
// ─────────────────────────────────────────────────────────────────────────

const canvas = document.getElementById('sky-canvas');
const container = document.getElementById('sky-canvas-container');

const scene = new THREE.Scene();
scene.background = null;

const camera = new THREE.PerspectiveCamera(
  60, container.clientWidth / container.clientHeight, 0.1, 5000
);
// Camera at small offset from origin (OrbitControls needs nonzero
// target-camera distance). Looking south by default, slightly above horizon.
// The celestial sphere is at radius 800; from anywhere this close to origin
// the parallax is negligible.
camera.position.set(0, 0, 0.5);
camera.lookAt(0, 0, -1);

const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  alpha: true,
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(container.clientWidth, container.clientHeight);

const controls = new OrbitControls(camera, canvas);
controls.target.set(0, 0, 0);
controls.enableZoom = false;
controls.enablePan = false;
controls.enabled = false;  // Sabbath default
controls.rotateSpeed = 0.25;
controls.minPolarAngle = Math.PI * 0.10;
controls.maxPolarAngle = Math.PI * 0.50;  // can't tilt below horizon

// ─────────────────────────────────────────────────────────────────────────
// Celestial sphere group: built once in equatorial coords, rotated each
// frame to align with the observer's local horizon at current time.
// ─────────────────────────────────────────────────────────────────────────

const celestialSphere = new THREE.Group();
scene.add(celestialSphere);

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

  // Reset, then rotate. Y first (LST), then X (polar tilt).
  // Y rotation by -LST brings the local meridian to the -Z (south) direction.
  // X rotation by +(π/2 − lat) tilts the celestial pole to altitude = lat
  // in the +Z (north) direction.
  celestialSphere.rotation.set(0, 0, 0);
  celestialSphere.rotateOnWorldAxis(new THREE.Vector3(0, 1, 0), -lstRad);
  celestialSphere.rotateOnWorldAxis(new THREE.Vector3(1, 0, 0), Math.PI / 2 - latRad);
}

// ─────────────────────────────────────────────────────────────────────────
// Star color from B-V color index
// ─────────────────────────────────────────────────────────────────────────

function ciToColor(ci) {
  let r, g, b;
  if (ci < -0.3)      { r = 0.65; g = 0.75; b = 1.0;  }  // blue (Rigel)
  else if (ci < 0.0)  { r = 0.80; g = 0.88; b = 1.0;  }  // blue-white (Vega)
  else if (ci < 0.3)  { r = 1.0;  g = 0.98; b = 0.95; }  // white (Sirius)
  else if (ci < 0.6)  { r = 1.0;  g = 0.95; b = 0.78; }  // yellow-white (Sun)
  else if (ci < 1.0)  { r = 1.0;  g = 0.86; b = 0.62; }  // yellow (Arcturus)
  else if (ci < 1.5)  { r = 1.0;  g = 0.74; b = 0.45; }  // orange (Aldebaran)
  else                { r = 1.0;  g = 0.55; b = 0.38; }  // red (Antares)
  return new THREE.Color(r, g, b);
}

function magToSize(mag) {
  const t = Math.max(0, Math.min(1, (MAG_DIMMEST - mag) / (MAG_DIMMEST - MAG_BRIGHTEST)));
  return POINT_SIZE_MIN + (POINT_SIZE_MAX - POINT_SIZE_MIN) * Math.pow(t, 2.0);
}

function magToOpacity(mag) {
  const t = Math.max(0, Math.min(1, (MAG_DIMMEST - mag) / (MAG_DIMMEST - MAG_BRIGHTEST)));
  return 0.45 + 0.55 * t;
}

// ─────────────────────────────────────────────────────────────────────────
// Star texture
// ─────────────────────────────────────────────────────────────────────────

function makeStarTexture() {
  const size = 64;
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  grad.addColorStop(0.0,  'rgba(255,255,255,1)');
  grad.addColorStop(0.25, 'rgba(255,255,255,0.65)');
  grad.addColorStop(0.55, 'rgba(255,255,255,0.18)');
  grad.addColorStop(1.0,  'rgba(255,255,255,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(c);
  tex.needsUpdate = true;
  return tex;
}
const starTexture = makeStarTexture();

// ─────────────────────────────────────────────────────────────────────────
// Stars — built once in equatorial coords
// ─────────────────────────────────────────────────────────────────────────

function buildStars(stars) {
  const positions = [];
  const colors = [];
  const sizes = [];

  for (const star of stars) {
    const pos = equatorialToCartesian(star.ra, star.dec);
    positions.push(pos.x, pos.y, pos.z);

    const color = ciToColor(star.ci || 0);
    const opacity = magToOpacity(star.mag);
    colors.push(color.r * opacity, color.g * opacity, color.b * opacity);
    sizes.push(magToSize(star.mag));
  }

  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geom.setAttribute('aColor',   new THREE.Float32BufferAttribute(colors, 3));
  geom.setAttribute('aSize',    new THREE.Float32BufferAttribute(sizes, 1));

  // Custom shader — note: we declare our own attribute names (aColor, aSize)
  // to avoid any auto-injection magic from three.js. Position is the only
  // attribute three.js always provides.
  const material = new THREE.ShaderMaterial({
    uniforms: {
      pointTexture: { value: starTexture },
      pixelRatio:   { value: renderer.getPixelRatio() },
    },
    vertexShader: `
      attribute float aSize;
      attribute vec3 aColor;
      varying vec3 vColor;
      uniform float pixelRatio;
      void main() {
        vColor = aColor;
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = aSize * pixelRatio * (300.0 / max(1.0, -mvPosition.z));
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      uniform sampler2D pointTexture;
      varying vec3 vColor;
      void main() {
        vec4 tex = texture2D(pointTexture, gl_PointCoord);
        gl_FragColor = vec4(vColor, 1.0) * tex;
        if (gl_FragColor.a < 0.02) discard;
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });

  const points = new THREE.Points(geom, material);
  celestialSphere.add(points);
  console.log(`[sky] built ${stars.length} stars`);
  return points;
}

// ─────────────────────────────────────────────────────────────────────────
// Label sprites (sign names, heteronyms, canonical texts)
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

let currentMode = 'sabbath';
function setMode(mode) {
  currentMode = mode;
  controls.enabled = (mode === 'merkabah');
}

// ─────────────────────────────────────────────────────────────────────────
// Resize
// ─────────────────────────────────────────────────────────────────────────

function onResize() {
  const w = container.clientWidth;
  const h = container.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
}
window.addEventListener('resize', onResize);

// ─────────────────────────────────────────────────────────────────────────
// Animation
// ─────────────────────────────────────────────────────────────────────────

function animate() {
  requestAnimationFrame(animate);
  applyCelestialAlignment(new Date());
  controls.update();
  renderer.render(scene, camera);
}

// ─────────────────────────────────────────────────────────────────────────
// Boot
// ─────────────────────────────────────────────────────────────────────────

async function boot() {
  try {
    console.log(`[sky] booting — observer ${OBSERVER.name} (${OBSERVER.lat}, ${OBSERVER.lng})`);
    const [stars, zodiac] = await Promise.all([
      fetch('/sky/stars.json').then(r => { if (!r.ok) throw new Error(`stars.json ${r.status}`); return r.json(); }),
      fetch('/sky/zodiac.json').then(r => { if (!r.ok) throw new Error(`zodiac.json ${r.status}`); return r.json(); }),
    ]);

    buildStars(stars);
    buildZodiacLabels(zodiac);
    buildCanonicalLabels(zodiac, stars);

    window.sky = { setMode, observer: OBSERVER };
    window.dispatchEvent(new CustomEvent('sky-ready', {
      detail: { starCount: stars.length, observer: OBSERVER },
    }));

    animate();
    console.log('[sky] booted');
  } catch (e) {
    console.error('[sky] boot failed:', e);
  }
}

boot();
