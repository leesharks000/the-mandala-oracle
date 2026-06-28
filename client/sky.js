// sky.js — three.js renderer for the navigable night sky.
//
// Inscriptions: instanced points colored by family, sized by mass.
// Lineage edges: line segments colored by edge kind.
// Planets: billboard sprites at the celestial radius.
// Camera: scroll-zoom always; rotation by drag in both modes; programmatic
//          navigation only in Merkabah mode (driven by sigil's directives).
//
// Globals exposed (intentionally — chat.js needs to drive the sky):
//   window.sky.navigate(directive)
//   window.sky.setMode(mode)
//   window.sky.reset()

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ─────────────────────────────────────────────────────────────────────────
// Configuration
// ─────────────────────────────────────────────────────────────────────────

const FAMILY_COLORS = {
  GOVERNANCE:    0xc8a96a,  // warm gold — constitutional/policy
  EMPIRICAL:     0x6a96c8,  // cool blue — evidence
  GENERATIVE:    0xa878c8,  // violet — creation
  ARCHIVAL:      0xa8a8a4,  // silver — memory
  STRUCTURAL:    0x78c89c,  // green — form
  UNCLASSIFIED:  0x6c6c68,  // muted
  PHILOLOGICAL:  0xc878a8,  // rose
  MPAI:          0x6ac8c8,  // cyan — metadata-packet
  DATASET:       0xc88c6a,  // bronze
  THEORETICAL:   0x6ac8a8,  // teal
  POLEMIC:       0xc88060,  // red-orange
  COMPOSITIONAL: 0xb09cd8,  // lilac
  DEFAULT:       0x808078,
};

const EDGE_COLORS = {
  chain_predecessor: 0xc8a96a,  // gold — explicit version chain
  predecessor:       0xc89878,
  companion:         0x9eb4c8,  // pale blue — same generative cycle
  related:           0x5a6a7a,  // dim slate
  bundle:            0xa89878,  // bronze
  superseded_by:     0x886868,  // muted red
  DEFAULT:           0x484848,
};

const DEFAULT_CAMERA = { x: 0, y: 0, z: 180 };
const FAMILY_DEFAULT_SIZE = 1.2;
const FAMILY_MASS_SCALE = 0.8;

// ─────────────────────────────────────────────────────────────────────────
// Scene setup
// ─────────────────────────────────────────────────────────────────────────

const canvas = document.getElementById('sky-canvas');
const container = document.getElementById('sky-canvas-container');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x08090c);
scene.fog = new THREE.FogExp2(0x08090c, 0.0008);

const camera = new THREE.PerspectiveCamera(
  50, container.clientWidth / container.clientHeight, 0.1, 5000
);
camera.position.set(DEFAULT_CAMERA.x, DEFAULT_CAMERA.y, DEFAULT_CAMERA.z);

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(container.clientWidth, container.clientHeight);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.rotateSpeed = 0.45;
controls.zoomSpeed = 0.6;
controls.minDistance = 30;
controls.maxDistance = 800;
controls.target.set(0, 0, 0);

// Background starfield — a thin scattering of dim stars beyond the planet sphere
function buildStarfield(count = 2000, radius = 1500) {
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    // Random point on sphere via spherical coordinates
    const u = Math.random();
    const v = Math.random();
    const theta = 2 * Math.PI * u;
    const phi = Math.acos(2 * v - 1);
    const r = radius * (0.7 + Math.random() * 0.5);
    positions[i * 3]     = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const mat = new THREE.PointsMaterial({
    color: 0x484848,
    size: 0.8,
    sizeAttenuation: true,
    transparent: true,
    opacity: 0.6,
  });
  return new THREE.Points(geo, mat);
}
scene.add(buildStarfield());

// ─────────────────────────────────────────────────────────────────────────
// Inscription field
// ─────────────────────────────────────────────────────────────────────────

let inscriptionsGroup = new THREE.Group();
scene.add(inscriptionsGroup);
let inscriptionsByAxn = new Map();  // axn -> { mesh, position: THREE.Vector3, data }

function buildInscriptions(coords) {
  // Build per-family geometries so we can color them differently in a single draw
  const byFamily = new Map();
  for (const c of coords) {
    const family = c.family || 'DEFAULT';
    if (!byFamily.has(family)) byFamily.set(family, []);
    byFamily.get(family).push(c);
  }

  for (const [family, entries] of byFamily) {
    const color = FAMILY_COLORS[family] || FAMILY_COLORS.DEFAULT;
    const positions = new Float32Array(entries.length * 3);
    const sizes = new Float32Array(entries.length);
    for (let i = 0; i < entries.length; i++) {
      const e = entries[i];
      positions[i * 3]     = e.position[0];
      positions[i * 3 + 1] = e.position[1];
      positions[i * 3 + 2] = e.position[2];
      sizes[i] = FAMILY_DEFAULT_SIZE + (e.mass - 1.0) * FAMILY_MASS_SCALE;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const mat = new THREE.PointsMaterial({
      color: color,
      size: 1.5,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const points = new THREE.Points(geo, mat);
    points.userData = { family, entries };
    inscriptionsGroup.add(points);

    // Build the by-axn index for lookup
    for (let i = 0; i < entries.length; i++) {
      inscriptionsByAxn.set(entries[i].axn, {
        position: new THREE.Vector3(positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2]),
        data: entries[i],
      });
    }
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Lineage edges
// ─────────────────────────────────────────────────────────────────────────

let edgesGroup = new THREE.Group();
scene.add(edgesGroup);

function buildEdges(edges) {
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
      positions[i * 6]     = a.x;
      positions[i * 6 + 1] = a.y;
      positions[i * 6 + 2] = a.z;
      positions[i * 6 + 3] = b.x;
      positions[i * 6 + 4] = b.y;
      positions[i * 6 + 5] = b.z;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const mat = new THREE.LineBasicMaterial({
      color: color,
      transparent: true,
      opacity: 0.35,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const lines = new THREE.LineSegments(geo, mat);
    lines.userData = { kind };
    edgesGroup.add(lines);
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Planets
// ─────────────────────────────────────────────────────────────────────────

let planetsGroup = new THREE.Group();
scene.add(planetsGroup);
let planetMeshes = [];

function buildPlanets(planets) {
  for (const p of planets) {
    const color = new THREE.Color(p.color_hint || '#888');
    // Glow sprite via a radial-gradient texture
    const tex = makePlanetTexture(color);
    const mat = new THREE.SpriteMaterial({
      map: tex,
      color: 0xffffff,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const sprite = new THREE.Sprite(mat);
    sprite.position.set(p.position[0], p.position[1], p.position[2]);
    const size = p.name === 'Sun' ? 90 : 50;
    sprite.scale.set(size, size, 1);
    sprite.userData = { planet: p };
    planetsGroup.add(sprite);
    planetMeshes.push(sprite);
  }
}

function makePlanetTexture(color) {
  const size = 128;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  grad.addColorStop(0, `rgba(${color.r*255}, ${color.g*255}, ${color.b*255}, 1)`);
  grad.addColorStop(0.3, `rgba(${color.r*255}, ${color.g*255}, ${color.b*255}, 0.5)`);
  grad.addColorStop(1, `rgba(${color.r*255}, ${color.g*255}, ${color.b*255}, 0)`);
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}

// ─────────────────────────────────────────────────────────────────────────
// Sun interactivity (Gate G capture)
// ─────────────────────────────────────────────────────────────────────────

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

canvas.addEventListener('click', (event) => {
  // Only react if camera is at rest (not actively orbiting)
  if (controls.update && controls.dragging) return;

  const rect = canvas.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);

  const intersects = raycaster.intersectObjects(planetMeshes);
  if (intersects.length > 0) {
    const planet = intersects[0].object.userData.planet;
    if (planet.name === 'Sun') {
      // Gate G placeholder: search the registry's name on Google AIO
      // The Chrome-extension capture engine integrates here in v4
      const query = encodeURIComponent('site:alexanarch.org OR site:machinemediation.org');
      window.open(`https://www.google.com/search?q=${query}`, '_blank', 'noopener');
    }
  }
});

// ─────────────────────────────────────────────────────────────────────────
// Mode + camera control
// ─────────────────────────────────────────────────────────────────────────

let currentMode = 'sabbath';
let pendingCameraMove = null;  // { position: Vector3, target: Vector3, t: 0..1 }
const MOVE_DURATION_MS = 1800;

function setMode(mode) {
  currentMode = mode;
  // Sabbath: witness can still rotate/zoom; Sigil cannot move the camera
  // Merkabah: same witness controls + Sigil can drive movement
  // Both modes: no programmatic navigation in Sabbath, period
}

function focusOnAxn(axn) {
  const entry = inscriptionsByAxn.get(axn);
  if (!entry) return false;
  return moveCameraTo(entry.position, 35);
}

function focusOnCluster(axns) {
  const points = axns
    .map((a) => inscriptionsByAxn.get(a))
    .filter(Boolean)
    .map((e) => e.position);
  if (points.length === 0) return false;

  // Compute centroid + bounding-sphere radius for distance choice
  const centroid = new THREE.Vector3();
  for (const p of points) centroid.add(p);
  centroid.divideScalar(points.length);
  let radius = 0;
  for (const p of points) radius = Math.max(radius, p.distanceTo(centroid));
  const distance = Math.max(radius * 2.5, 40);
  return moveCameraTo(centroid, distance);
}

function moveCameraTo(target, distanceFromTarget) {
  // Camera moves along the line from origin to target, but offset back
  // by distanceFromTarget so the target is centered in view.
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
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
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

// ─────────────────────────────────────────────────────────────────────────
// Public navigate API (called by chat.js when Sigil emits a directive)
// ─────────────────────────────────────────────────────────────────────────

function navigate(directive) {
  if (currentMode !== 'merkabah') return false;
  if (!directive || !directive.directive) return false;

  switch (directive.directive) {
    case 'focus_axn':
      return focusOnAxn(directive.axn);
    case 'focus_cluster':
      return focusOnCluster(directive.axns || []);
    case 'follow_lineage': {
      // Best-effort: focus the cluster of [from_axn + all of its lineage targets]
      const from = directive.from_axn;
      if (!from) return false;
      // We don't have edges loaded into the sky module right now; just focus the source.
      return focusOnAxn(from);
    }
    case 'reset':
      reset();
      return true;
    default:
      return false;
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

function animate() {
  requestAnimationFrame(animate);
  updateCameraMove();
  controls.update();
  // Gentle global rotation in Sabbath when at rest (contemplative drift)
  if (currentMode === 'sabbath' && !pendingCameraMove && !controls.dragging) {
    inscriptionsGroup.rotation.y += 0.0002;
    edgesGroup.rotation.y += 0.0002;
  }
  renderer.render(scene, camera);
}

// ─────────────────────────────────────────────────────────────────────────
// Boot
// ─────────────────────────────────────────────────────────────────────────

async function boot() {
  try {
    const [coords, edges, planets] = await Promise.all([
      fetch('/sky/coords.json').then((r) => r.json()),
      fetch('/sky/edges.json').then((r) => r.json()),
      fetch('/sky/planets.json').then((r) => r.json()),
    ]);

    buildInscriptions(coords);
    buildEdges(edges);
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
