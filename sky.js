// sky.js — full-viewport night sky.
//
// In the new framing (script reframe of 2026-06-28):
//   - The night sky is the CANON: primary texts as stars (Revelation, Whitman,
//     Sappho, eventually Lee Sharks's own primary works). These are not yet
//     populated; the canon-as-stars layer will be added in subsequent cycles.
//   - The alexanarch corpus (cha) is the INVISIBLE SUBSTRATE: it is what
//     Sigil channels, not what the witness sees as the sky. In v1.2 we render
//     it as a very dim background of small points — visible as "the wisdom
//     underneath," but emphatically not the foreground.
//   - The seven planets are the CELESTIAL SUBSTRATE-ROLE OFFICES (AXN-0237).
//     They remain the prominent celestial bodies.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ─────────────────────────────────────────────────────────────────────────
// Configuration
// ─────────────────────────────────────────────────────────────────────────

const FAMILY_COLORS = {
  GOVERNANCE:    0xc8a96a,
  EMPIRICAL:     0x6a96c8,
  GENERATIVE:    0xa878c8,
  ARCHIVAL:      0xa8a8a4,
  STRUCTURAL:    0x78c89c,
  UNCLASSIFIED:  0x6c6c68,
  PHILOLOGICAL:  0xc878a8,
  MPAI:          0x6ac8c8,
  DATASET:       0xc88c6a,
  THEORETICAL:   0x6ac8a8,
  POLEMIC:       0xc88060,
  COMPOSITIONAL: 0xb09cd8,
  DEFAULT:       0x808078,
};

const EDGE_COLORS = {
  chain_predecessor: 0xc8a96a,
  predecessor:       0xc89878,
  companion:         0x9eb4c8,
  related:           0x5a6a7a,
  bundle:            0xa89878,
  superseded_by:     0x886868,
  DEFAULT:           0x484848,
};

const DEFAULT_CAMERA = { x: 0, y: 0, z: 220 };

// Cha-as-substrate visual constants — these are background, not foreground
const CHA_POINT_BASE_SIZE = 0.55;
const CHA_POINT_OPACITY = 0.32;
const CHA_EDGE_OPACITY = 0.12;

// Starfield background — multiple layers for depth
const STARFIELD_LAYERS = [
  { count: 1800, radius: 1400, sizeRange: [0.5, 1.4], brightnessRange: [0.35, 0.55] },
  { count: 600,  radius: 1200, sizeRange: [1.2, 2.6], brightnessRange: [0.55, 0.85] },
  { count: 120,  radius: 1000, sizeRange: [2.4, 4.0], brightnessRange: [0.75, 1.0]  },
];

// ─────────────────────────────────────────────────────────────────────────
// Scene
// ─────────────────────────────────────────────────────────────────────────

const canvas = document.getElementById('sky-canvas');
const container = document.getElementById('sky-canvas-container');

const scene = new THREE.Scene();
scene.background = null;  // CSS gradient shows through; keep canvas transparent
scene.fog = new THREE.FogExp2(0x050608, 0.00065);

const camera = new THREE.PerspectiveCamera(
  55, container.clientWidth / container.clientHeight, 0.1, 5000
);
camera.position.set(DEFAULT_CAMERA.x, DEFAULT_CAMERA.y, DEFAULT_CAMERA.z);

const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  alpha: true,            // transparent canvas so CSS gradient shows through
  premultipliedAlpha: false,
});
renderer.setClearColor(0x000000, 0);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(container.clientWidth, container.clientHeight);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.rotateSpeed = 0.4;
controls.zoomSpeed = 0.5;
controls.minDistance = 60;
controls.maxDistance = 900;
controls.enablePan = false;  // celestial sphere navigation only
controls.target.set(0, 0, 0);

let isDragging = false;
controls.addEventListener('start', () => { isDragging = true; });
controls.addEventListener('end', () => {
  setTimeout(() => { isDragging = false; }, 50);
});

// ─────────────────────────────────────────────────────────────────────────
// Procedural starfield — multi-layer for parallax depth
// ─────────────────────────────────────────────────────────────────────────

function makeStarTexture() {
  // Soft round star with a hot center and atmospheric halo
  const size = 64;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  grad.addColorStop(0,    'rgba(255, 255, 255, 1)');
  grad.addColorStop(0.15, 'rgba(255, 250, 230, 0.9)');
  grad.addColorStop(0.4,  'rgba(220, 220, 240, 0.35)');
  grad.addColorStop(1,    'rgba(255, 255, 255, 0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}

const starTexture = makeStarTexture();

function buildStarfieldLayer({ count, radius, sizeRange, brightnessRange }) {
  const positions = new Float32Array(count * 3);
  const sizes = new Float32Array(count);
  const brightnesses = new Float32Array(count);
  const phases = new Float32Array(count);  // for twinkle

  for (let i = 0; i < count; i++) {
    const u = Math.random();
    const v = Math.random();
    const theta = 2 * Math.PI * u;
    const phi = Math.acos(2 * v - 1);
    const r = radius * (0.85 + Math.random() * 0.3);
    positions[i*3]     = r * Math.sin(phi) * Math.cos(theta);
    positions[i*3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i*3 + 2] = r * Math.cos(phi);
    sizes[i] = sizeRange[0] + Math.random() * (sizeRange[1] - sizeRange[0]);
    brightnesses[i] = brightnessRange[0] + Math.random() * (brightnessRange[1] - brightnessRange[0]);
    phases[i] = Math.random() * Math.PI * 2;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  geo.setAttribute('brightness', new THREE.BufferAttribute(brightnesses, 1));
  geo.setAttribute('phase', new THREE.BufferAttribute(phases, 1));

  // Custom shader so each star has its own brightness + twinkle
  const mat = new THREE.ShaderMaterial({
    uniforms: {
      time: { value: 0 },
      pointTexture: { value: starTexture },
    },
    vertexShader: `
      attribute float size;
      attribute float brightness;
      attribute float phase;
      uniform float time;
      varying float vBrightness;
      void main() {
        float twinkle = 0.85 + 0.15 * sin(time * 0.7 + phase * 5.0);
        vBrightness = brightness * twinkle;
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = size * (300.0 / -mv.z);
        gl_Position = projectionMatrix * mv;
      }
    `,
    fragmentShader: `
      uniform sampler2D pointTexture;
      varying float vBrightness;
      void main() {
        vec4 tex = texture2D(pointTexture, gl_PointCoord);
        gl_FragColor = vec4(tex.rgb, tex.a * vBrightness);
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });

  return new THREE.Points(geo, mat);
}

const starfieldLayers = STARFIELD_LAYERS.map(buildStarfieldLayer);
starfieldLayers.forEach(layer => scene.add(layer));

// ─────────────────────────────────────────────────────────────────────────
// Cha-as-substrate (dim background of alexanarch corpus)
// ─────────────────────────────────────────────────────────────────────────

let chaGroup = new THREE.Group();
scene.add(chaGroup);
let inscriptionsByAxn = new Map();

function buildChaSubstrate(coords) {
  const byFamily = new Map();
  for (const c of coords) {
    const family = c.family || 'DEFAULT';
    if (!byFamily.has(family)) byFamily.set(family, []);
    byFamily.get(family).push(c);
  }

  for (const [family, entries] of byFamily) {
    const color = FAMILY_COLORS[family] || FAMILY_COLORS.DEFAULT;
    const positions = new Float32Array(entries.length * 3);
    for (let i = 0; i < entries.length; i++) {
      positions[i*3]     = entries[i].position[0];
      positions[i*3 + 1] = entries[i].position[1];
      positions[i*3 + 2] = entries[i].position[2];
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const mat = new THREE.PointsMaterial({
      color: color,
      size: CHA_POINT_BASE_SIZE,
      sizeAttenuation: true,
      transparent: true,
      opacity: CHA_POINT_OPACITY,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const points = new THREE.Points(geo, mat);
    points.userData = { family, layer: 'cha-substrate' };
    chaGroup.add(points);

    for (let i = 0; i < entries.length; i++) {
      inscriptionsByAxn.set(entries[i].axn, {
        position: new THREE.Vector3(positions[i*3], positions[i*3+1], positions[i*3+2]),
        data: entries[i],
      });
    }
  }
}

let chaEdgesGroup = new THREE.Group();
scene.add(chaEdgesGroup);

function buildChaEdges(edges) {
  const byKind = new Map();
  for (const e of edges) {
    const from = inscriptionsByAxn.get(e.from);
    const to = inscriptionsByAxn.get(e.to);
    if (!from || !to) continue;
    const kind = e.kind || 'DEFAULT';
    if (!byKind.has(kind)) byKind.set(kind, []);
    byKind.get(kind).push([from.position, to.position]);
  }

  for (const [kind, pairs] of byKind) {
    const color = EDGE_COLORS[kind] || EDGE_COLORS.DEFAULT;
    const positions = new Float32Array(pairs.length * 6);
    for (let i = 0; i < pairs.length; i++) {
      const [a, b] = pairs[i];
      positions[i*6]     = a.x;  positions[i*6+1] = a.y;  positions[i*6+2] = a.z;
      positions[i*6+3]   = b.x;  positions[i*6+4] = b.y;  positions[i*6+5] = b.z;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const mat = new THREE.LineBasicMaterial({
      color: color,
      transparent: true,
      opacity: CHA_EDGE_OPACITY,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    chaEdgesGroup.add(new THREE.LineSegments(geo, mat));
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Planets — the celestial substrate-role offices, prominent
// ─────────────────────────────────────────────────────────────────────────

let planetsGroup = new THREE.Group();
scene.add(planetsGroup);
let planetMeshes = [];

function makePlanetTexture(colorHex, name) {
  // Atmospheric body with a hot core and soft falloff. For prominent planets
  // (Sun in particular) the gradient is more luminous.
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  const color = new THREE.Color(colorHex);
  const r = Math.floor(color.r * 255);
  const g = Math.floor(color.g * 255);
  const b = Math.floor(color.b * 255);
  const isSun = name === 'Sun';
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  if (isSun) {
    grad.addColorStop(0,    `rgba(255, 252, 220, 1)`);
    grad.addColorStop(0.12, `rgba(${Math.min(r+30,255)}, ${Math.min(g+20,255)}, ${b}, 0.95)`);
    grad.addColorStop(0.35, `rgba(${r}, ${g}, ${b}, 0.6)`);
    grad.addColorStop(0.65, `rgba(${r}, ${g}, ${b}, 0.18)`);
    grad.addColorStop(1,    `rgba(${r}, ${g}, ${b}, 0)`);
  } else {
    grad.addColorStop(0,    `rgba(255, 255, 255, 0.95)`);
    grad.addColorStop(0.18, `rgba(${r}, ${g}, ${b}, 0.85)`);
    grad.addColorStop(0.45, `rgba(${r}, ${g}, ${b}, 0.4)`);
    grad.addColorStop(1,    `rgba(${r}, ${g}, ${b}, 0)`);
  }
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}

function buildPlanets(planets) {
  for (const p of planets) {
    const tex = makePlanetTexture(p.color_hint || '#888', p.name);
    const mat = new THREE.SpriteMaterial({
      map: tex,
      color: 0xffffff,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const sprite = new THREE.Sprite(mat);
    sprite.position.set(p.position[0], p.position[1], p.position[2]);
    const size = p.name === 'Sun' ? 130 : 75;
    sprite.scale.set(size, size, 1);
    sprite.userData = { planet: p };
    planetsGroup.add(sprite);
    planetMeshes.push(sprite);
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Sun interactivity (Gate G capture placeholder)
// ─────────────────────────────────────────────────────────────────────────

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

canvas.addEventListener('click', (event) => {
  if (isDragging) return;
  const rect = canvas.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);

  const intersects = raycaster.intersectObjects(planetMeshes);
  if (intersects.length > 0) {
    const planet = intersects[0].object.userData.planet;
    if (planet.name === 'Sun') {
      const query = encodeURIComponent('site:alexanarch.org OR site:machinemediation.org');
      window.open(`https://www.google.com/search?q=${query}`, '_blank', 'noopener');
    }
  }
});

// ─────────────────────────────────────────────────────────────────────────
// Mode + camera control
// ─────────────────────────────────────────────────────────────────────────

let currentMode = 'sabbath';
let pendingCameraMove = null;
const MOVE_DURATION_MS = 1800;

function setMode(mode) { currentMode = mode; }

function focusOnAxn(axn) {
  const entry = inscriptionsByAxn.get(axn);
  if (!entry) return false;
  return moveCameraTo(entry.position, 50);
}

function focusOnCluster(axns) {
  const points = axns.map(a => inscriptionsByAxn.get(a)).filter(Boolean).map(e => e.position);
  if (points.length === 0) return false;
  const centroid = new THREE.Vector3();
  for (const p of points) centroid.add(p);
  centroid.divideScalar(points.length);
  let radius = 0;
  for (const p of points) radius = Math.max(radius, p.distanceTo(centroid));
  return moveCameraTo(centroid, Math.max(radius * 2.5, 60));
}

function moveCameraTo(target, distanceFromTarget) {
  const dir = target.clone().normalize();
  if (dir.lengthSq() < 0.01) dir.set(0, 0, 1);
  const newCamPos = target.clone().add(dir.multiplyScalar(distanceFromTarget));
  pendingCameraMove = {
    fromPos: camera.position.clone(),
    toPos: newCamPos,
    fromTarget: controls.target.clone(),
    toTarget: target.clone(),
    startTime: performance.now(),
  };
  return true;
}

function reset() {
  pendingCameraMove = {
    fromPos: camera.position.clone(),
    toPos: new THREE.Vector3(DEFAULT_CAMERA.x, DEFAULT_CAMERA.y, DEFAULT_CAMERA.z),
    fromTarget: controls.target.clone(),
    toTarget: new THREE.Vector3(0, 0, 0),
    startTime: performance.now(),
  };
}

function easeInOutCubic(t) {
  return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
}

function updateCameraMove() {
  if (!pendingCameraMove) return;
  const elapsed = performance.now() - pendingCameraMove.startTime;
  const t = Math.min(1, elapsed / MOVE_DURATION_MS);
  const eased = easeInOutCubic(t);
  camera.position.lerpVectors(pendingCameraMove.fromPos, pendingCameraMove.toPos, eased);
  controls.target.lerpVectors(pendingCameraMove.fromTarget, pendingCameraMove.toTarget, eased);
  if (t >= 1) pendingCameraMove = null;
}

function navigate(directive) {
  if (currentMode !== 'merkabah') return false;
  if (!directive || !directive.directive) return false;
  switch (directive.directive) {
    case 'focus_axn':     return focusOnAxn(directive.axn);
    case 'focus_cluster': return focusOnCluster(directive.axns || []);
    case 'follow_lineage':
      if (!directive.from_axn) return false;
      return focusOnAxn(directive.from_axn);
    case 'reset':         reset(); return true;
    default:              return false;
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Animation + resize
// ─────────────────────────────────────────────────────────────────────────

function onResize() {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
}
window.addEventListener('resize', onResize);

const startTime = performance.now();
function animate() {
  requestAnimationFrame(animate);
  const elapsed = (performance.now() - startTime) / 1000;

  // Twinkle: update star shader time uniform
  for (const layer of starfieldLayers) {
    if (layer.material.uniforms) {
      layer.material.uniforms.time.value = elapsed;
    }
  }

  // Slow celestial drift — the heavens turn slowly above the reading
  if (currentMode === 'sabbath' && !pendingCameraMove && !isDragging) {
    chaGroup.rotation.y += 0.00008;
    chaEdgesGroup.rotation.y += 0.00008;
    // The starfield itself drifts very slightly — outer slowest, inner fastest
    starfieldLayers[0].rotation.y += 0.00002;
    starfieldLayers[1].rotation.y += 0.00004;
    starfieldLayers[2].rotation.y += 0.00006;
  }

  updateCameraMove();
  controls.update();
  renderer.render(scene, camera);
}

// ─────────────────────────────────────────────────────────────────────────
// Boot
// ─────────────────────────────────────────────────────────────────────────

async function boot() {
  try {
    const [coords, edges, planets] = await Promise.all([
      fetch('/sky/coords.json').then(r => r.json()),
      fetch('/sky/edges.json').then(r => r.json()),
      fetch('/sky/planets.json').then(r => r.json()),
    ]);

    buildChaSubstrate(coords);
    buildChaEdges(edges);
    buildPlanets(planets);

    window.sky = { navigate, setMode, reset };
    window.dispatchEvent(new CustomEvent('sky-ready', {
      detail: { inscriptionCount: coords.length, edgeCount: edges.length },
    }));

    animate();
  } catch (e) {
    console.error('Sky boot failed:', e);
  }
}

boot();
