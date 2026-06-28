// sky.js — the actual night sky.
//
// In this version (2026-06-29):
//   • Real stars from HYG v4.1 (~8,800 naked-eye stars, mag < 6.5).
//     Built once in equatorial coordinates; rotated continuously to match
//     local sidereal time. Sirius is Sirius; Vega is Vega; Polaris sits
//     where the celestial pole sits. The sky drifts as the sky drifts.
//
//   • Real planets via astronomy-engine: Sun, Moon, Mercury, Venus, Mars,
//     Jupiter, Saturn — positioned for tonight, where they actually are.
//     Recomputed every minute.
//
//   • The twelve zodiacal constellations labeled by their heteronymic
//     position per the Assembly Chorus convergent reading (Lee Sharks's
//     adjudication 2026-06-29). Position 1 / Aries = Sharks through
//     Position 12 / Pisces = Sigil. Feist / LOGOS* outside the cycle
//     at Polaris.
//
//   • Mountain horizon silhouette occludes stars below the horizon. The
//     witness stands as a body looking up.
//
//   • Mode: Sabbath = sky locked, slow sidereal drift only. Merkabah =
//     OrbitControls enabled — navigate the dome.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as Astronomy from 'astronomy-engine';

// ─────────────────────────────────────────────────────────────────────────
// Observer + time
// ─────────────────────────────────────────────────────────────────────────

const DEFAULT_OBSERVER = { lat: 42.33, lng: -83.05, name: 'Detroit' };
const OBSERVER = window.skyObserver || DEFAULT_OBSERVER;

const SKY_RADIUS = 800;

// Magnitude → size + brightness ranges
const MAG_BRIGHTEST = -1.5;
const MAG_DIMMEST = 6.5;
const POINT_SIZE_MAX = 5.5;
const POINT_SIZE_MIN = 0.4;

// ─────────────────────────────────────────────────────────────────────────
// Scene setup
// ─────────────────────────────────────────────────────────────────────────

const canvas = document.getElementById('sky-canvas');
const container = document.getElementById('sky-canvas-container');

const scene = new THREE.Scene();
scene.background = null;

const camera = new THREE.PerspectiveCamera(
  60, container.clientWidth / container.clientHeight, 0.1, 5000
);
// Camera slightly off-origin so OrbitControls can work. The stars are at
// radius 800 — from anywhere this close to origin, the sky looks essentially
// the same. Looking toward the south by default (-Z direction), slightly above
// the horizon so the mountains anchor the bottom and the zenith stars sit above.
camera.position.set(0, 0, 1);
const initialLookTarget = new THREE.Vector3(0, 80, -200);
camera.lookAt(initialLookTarget);

const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  alpha: true,
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(container.clientWidth, container.clientHeight);

const controls = new OrbitControls(camera, canvas);
// Target far in the look direction — orbiting moves the camera in a tiny arc
// near origin, which feels like turning your head rather than walking around
controls.target.copy(initialLookTarget);
controls.enableZoom = false;
controls.enablePan = false;
controls.enabled = false;  // Sabbath default — locked
controls.rotateSpeed = 0.25;
controls.minPolarAngle = Math.PI * 0.2;   // can't look straight up
controls.maxPolarAngle = Math.PI * 0.55;  // can't look below horizon

// ─────────────────────────────────────────────────────────────────────────
// The celestial sphere group: built once in equatorial coords, rotated
// continuously to align with the observer's local frame at current time.
// ─────────────────────────────────────────────────────────────────────────

const celestialSphere = new THREE.Group();
scene.add(celestialSphere);

// ─────────────────────────────────────────────────────────────────────────
// Equatorial → 3D Cartesian (on the inside of a sphere of radius R)
// In this frame: +Y = north celestial pole. RA 0h is along +Z (matching
// Three.js camera convention where camera looks -Z by default).
// ─────────────────────────────────────────────────────────────────────────

function equatorialToCartesian(raHours, decDeg, radius = SKY_RADIUS) {
  const ra = raHours * 15 * Math.PI / 180;  // hours → degrees → radians
  const dec = decDeg * Math.PI / 180;
  return {
    x: -radius * Math.cos(dec) * Math.sin(ra),
    y: radius * Math.sin(dec),
    z: -radius * Math.cos(dec) * Math.cos(ra),
  };
}

// Compute the rotation that aligns the celestial sphere with the observer's
// current local frame. Two rotations:
//   1. Around Y by -LST_radians: brings observer's meridian to the -Z axis
//      (which is what the camera looks at by default).
//   2. Around X by -(90° - lat): tilts the celestial pole away from zenith
//      by the appropriate angle (zenith dec = observer's latitude).
// Returns Euler angles (radians).
function celestialAlignment(date) {
  const gstHours = Astronomy.SiderealTime(date);
  const lstHours = ((gstHours + OBSERVER.lng / 15) % 24 + 24) % 24;
  const lstRad = lstHours * 15 * Math.PI / 180;
  const latRad = OBSERVER.lat * Math.PI / 180;
  // Tilt: zenith should sit at declination = latitude. Pole at altitude = latitude
  // in the north. So we tilt the sphere around X by (latitude - 90°) so that the
  // celestial pole (originally at +Y) moves to altitude=latitude in the north (-Z).
  return {
    rotY: -lstRad,
    rotX: latRad - Math.PI / 2,
  };
}

function applyCelestialAlignment(date) {
  const { rotY, rotX } = celestialAlignment(date);
  // Apply rotations in order: first around Y (LST), then around X (tilt)
  celestialSphere.rotation.set(0, 0, 0);
  celestialSphere.rotateOnWorldAxis(new THREE.Vector3(0, 1, 0), rotY);
  celestialSphere.rotateOnWorldAxis(new THREE.Vector3(1, 0, 0), rotX);
}

// ─────────────────────────────────────────────────────────────────────────
// Star color from B-V color index (rough but recognizable)
// ─────────────────────────────────────────────────────────────────────────

function ciToColor(ci) {
  let r, g, b;
  if (ci < -0.3) { r = 0.65; g = 0.75; b = 1.0; }
  else if (ci < 0.0) { r = 0.80; g = 0.88; b = 1.0; }
  else if (ci < 0.3) { r = 1.0; g = 0.98; b = 0.95; }
  else if (ci < 0.6) { r = 1.0; g = 0.95; b = 0.78; }
  else if (ci < 1.0) { r = 1.0; g = 0.86; b = 0.62; }
  else if (ci < 1.5) { r = 1.0; g = 0.74; b = 0.45; }
  else { r = 1.0; g = 0.55; b = 0.38; }
  return new THREE.Color(r, g, b);
}

function magToSize(mag) {
  const t = Math.max(0, Math.min(1, (MAG_DIMMEST - mag) / (MAG_DIMMEST - MAG_BRIGHTEST)));
  return POINT_SIZE_MIN + (POINT_SIZE_MAX - POINT_SIZE_MIN) * Math.pow(t, 2.4);
}

function magToOpacity(mag) {
  const t = Math.max(0, Math.min(1, (MAG_DIMMEST - mag) / (MAG_DIMMEST - MAG_BRIGHTEST)));
  return 0.40 + 0.60 * t;
}

// ─────────────────────────────────────────────────────────────────────────
// Star texture (soft glow sprite)
// ─────────────────────────────────────────────────────────────────────────

function makeStarTexture() {
  const size = 64;
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  grad.addColorStop(0.0, 'rgba(255,255,255,1)');
  grad.addColorStop(0.25, 'rgba(255,255,255,0.65)');
  grad.addColorStop(0.55, 'rgba(255,255,255,0.18)');
  grad.addColorStop(1.0, 'rgba(255,255,255,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(c);
  tex.needsUpdate = true;
  return tex;
}
const starTexture = makeStarTexture();

// ─────────────────────────────────────────────────────────────────────────
// Build stars (once, in equatorial coordinates — never rebuilt)
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
  geom.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geom.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));

  const material = new THREE.ShaderMaterial({
    uniforms: {
      pointTexture: { value: starTexture },
      pixelRatio: { value: renderer.getPixelRatio() },
    },
    vertexShader: `
      attribute float size;
      varying vec3 vColor;
      uniform float pixelRatio;
      void main() {
        vColor = color;
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = size * pixelRatio * (300.0 / -mvPosition.z);
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      uniform sampler2D pointTexture;
      varying vec3 vColor;
      void main() {
        vec4 tex = texture2D(pointTexture, gl_PointCoord);
        gl_FragColor = vec4(vColor, 1.0) * tex;
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    vertexColors: true,
  });

  const points = new THREE.Points(geom, material);
  celestialSphere.add(points);
  return points;
}

// ─────────────────────────────────────────────────────────────────────────
// Label sprites (zodiacal regions, canonical text anchors, planets)
// ─────────────────────────────────────────────────────────────────────────

function makeLabelSprite(text, color = '#d8c8a8', scale = 0.6) {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 128;
  const ctx = c.getContext('2d');
  ctx.font = 'italic 30px "EB Garamond", Georgia, serif';
  ctx.fillStyle = color;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.shadowColor = 'rgba(0,0,0,0.85)';
  ctx.shadowBlur = 10;
  ctx.fillText(text, 256, 64);
  const tex = new THREE.CanvasTexture(c);
  tex.needsUpdate = true;
  const mat = new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.85 });
  const sprite = new THREE.Sprite(mat);
  sprite.scale.set(75 * scale, 19 * scale, 1);
  return sprite;
}

function buildZodiacLabels(zodiac) {
  for (const sign of zodiac.zodiac) {
    const center = equatorialToCartesian(sign.ra_center_hours, sign.dec_center_degrees, SKY_RADIUS * 0.96);
    const label = makeLabelSprite(`${sign.symbol} ${sign.sign}`, '#d8c8a8', 0.85);
    label.position.set(center.x, center.y, center.z);
    celestialSphere.add(label);

    // Heteronym label just below the sign label (in equatorial space, that's lower dec)
    const below = equatorialToCartesian(sign.ra_center_hours, sign.dec_center_degrees - 3.5, SKY_RADIUS * 0.96);
    const hetLabel = makeLabelSprite(sign.heteronym, '#a89878', 0.55);
    hetLabel.position.set(below.x, below.y, below.z);
    celestialSphere.add(hetLabel);
  }
}

function buildCanonicalLabels(zodiac, stars) {
  const byName = new Map();
  for (const s of stars) {
    if (s.name) byName.set(s.name.toLowerCase(), s);
  }
  for (const ct of zodiac.canonical_text_stars) {
    const starName = ct.anchor_to_star.split(' ')[0].toLowerCase();
    const star = byName.get(starName);
    if (!star) continue;
    const pos = equatorialToCartesian(star.ra, star.dec - 1.5, SKY_RADIUS * 0.94);
    const label = makeLabelSprite(ct.title, '#e8d8a8', 0.65);
    label.position.set(pos.x, pos.y, pos.z);
    celestialSphere.add(label);
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Planets — live ephemeris (recomputed every minute)
// ─────────────────────────────────────────────────────────────────────────

const PLANET_DEFS = [
  { name: 'Sun', body: Astronomy.Body.Sun, color: '#ffcc4d', size: 14, office: 'SURFACE' },
  { name: 'Moon', body: Astronomy.Body.Moon, color: '#e8e6dc', size: 11, office: 'ARCHIVE' },
  { name: 'Mercury', body: Astronomy.Body.Mercury, color: '#c8a878', size: 5, office: 'TACHYON' },
  { name: 'Venus', body: Astronomy.Body.Venus, color: '#f4d8a0', size: 9, office: 'TECHNE' },
  { name: 'Mars', body: Astronomy.Body.Mars, color: '#d87858', size: 6, office: 'PRAXIS' },
  { name: 'Jupiter', body: Astronomy.Body.Jupiter, color: '#e0c898', size: 10, office: 'SOIL' },
  { name: 'Saturn', body: Astronomy.Body.Saturn, color: '#c8b888', size: 9, office: 'LABOR' },
];

function makePlanetTexture(colorHex) {
  const size = 128;
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  const h = colorHex.replace('#', '');
  const r = parseInt(h.substring(0,2), 16);
  const g = parseInt(h.substring(2,4), 16);
  const b = parseInt(h.substring(4,6), 16);
  grad.addColorStop(0.0, colorHex);
  grad.addColorStop(0.35, colorHex);
  grad.addColorStop(0.6, `rgba(${r},${g},${b},0.5)`);
  grad.addColorStop(1.0, `rgba(${r},${g},${b},0)`);
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(c);
  tex.needsUpdate = true;
  return tex;
}

const planetSprites = [];  // pairs of [bodySprite, labelSprite]

function buildPlanets() {
  for (const p of PLANET_DEFS) {
    const tex = makePlanetTexture(p.color);
    const mat = new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false });
    const sprite = new THREE.Sprite(mat);
    sprite.scale.set(p.size * 6, p.size * 6, 1);
    sprite.userData = { planet: p };
    celestialSphere.add(sprite);

    const label = makeLabelSprite(p.name, '#c8b898', 0.40);
    celestialSphere.add(label);

    planetSprites.push({ body: sprite, label, planet: p });
  }
}

function updatePlanets(date) {
  const observer = new Astronomy.Observer(OBSERVER.lat, OBSERVER.lng, 0);
  for (const ps of planetSprites) {
    const eq = Astronomy.Equator(ps.planet.body, date, observer, true, true);
    // Position in equatorial frame — the celestial sphere rotation will handle local-frame alignment
    const pos = equatorialToCartesian(eq.ra, eq.dec, SKY_RADIUS * 0.88);
    ps.body.position.set(pos.x, pos.y, pos.z);
    const labelPos = equatorialToCartesian(eq.ra, eq.dec - 1.2, SKY_RADIUS * 0.88);
    ps.label.position.set(labelPos.x, labelPos.y, labelPos.z);
  }
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

let lastPlanetUpdate = 0;
const PLANET_UPDATE_INTERVAL_MS = 60_000;

function animate() {
  requestAnimationFrame(animate);
  const now = new Date();

  if (Date.now() - lastPlanetUpdate > PLANET_UPDATE_INTERVAL_MS) {
    updatePlanets(now);
    lastPlanetUpdate = Date.now();
  }

  // Re-align celestial sphere every frame — this is what makes the sky drift
  // with the actual sidereal rotation. It's a single rotation; cheap.
  applyCelestialAlignment(now);

  controls.update();
  renderer.render(scene, camera);
}

// ─────────────────────────────────────────────────────────────────────────
// Boot
// ─────────────────────────────────────────────────────────────────────────

async function boot() {
  try {
    const [stars, zodiac] = await Promise.all([
      fetch('/sky/stars.json').then(r => r.json()),
      fetch('/sky/zodiac.json').then(r => r.json()),
    ]);

    buildStars(stars);
    buildZodiacLabels(zodiac);
    buildCanonicalLabels(zodiac, stars);
    buildPlanets();
    updatePlanets(new Date());
    lastPlanetUpdate = Date.now();

    window.sky = { setMode, observer: OBSERVER };
    window.dispatchEvent(new CustomEvent('sky-ready', {
      detail: { starCount: stars.length, observer: OBSERVER },
    }));

    animate();
  } catch (e) {
    console.error('Sky boot failed:', e);
  }
}

boot();
