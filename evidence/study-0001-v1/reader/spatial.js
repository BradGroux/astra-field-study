import * as THREE from './vendor/three.module.js';

// A focused six-day profile prevents the occlusion of the former 18-project cube.
// The scale remains fixed to the full dataset, including when a filter is applied.
export async function createSpatial(container, data, onSelect) {
  await document.fonts.ready;
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setClearColor(0x121f30);
  container.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera();
  const group = new THREE.Group();
  scene.add(group, new THREE.AmbientLight(0xffffff, 2));
  const light = new THREE.DirectionalLight(0xffffff, 3);
  light.position.set(-5, 12, 9);
  scene.add(light);
  const maxima = Object.fromEntries(['responses', 'total_tokens', 'corrective_units']
    .map(key => [key, Math.max(1, ...data.rows.map(row => row[key]))]));
  let azimuth = 12, elevation = 18, objects = [];

  function draw() {
    const width = container.clientWidth, height = container.clientHeight;
    if (!width || !height) return;
    renderer.setSize(width, height);
    const a = THREE.MathUtils.degToRad(azimuth), e = THREE.MathUtils.degToRad(elevation);
    const target = new THREE.Vector3(0, 2.1, 0);
    camera.position.set(22 * Math.sin(a) * Math.cos(e), 2.1 + 22 * Math.sin(e), 22 * Math.cos(a) * Math.cos(e));
    camera.lookAt(target);
    camera.updateMatrixWorld();
    // Fit every supported camera angle to a fixed box, including labels and axis.
    // This preserves the apparent scale between project selections.
    let extentX = 0, extentY = 0;
    for (const x of [-6.4, 6.4]) for (const y of [-.8, 5.5]) for (const z of [-1.8, 1.8]) {
      const v = new THREE.Vector3(x, y, z).applyMatrix4(camera.matrixWorldInverse);
      extentX = Math.max(extentX, Math.abs(v.x));
      extentY = Math.max(extentY, Math.abs(v.y));
    }
    const aspect = width / height;
    const halfHeight = Math.max(extentY, extentX / aspect) * 1.04;
    camera.left = -halfHeight * aspect; camera.right = halfHeight * aspect;
    camera.top = halfHeight; camera.bottom = -halfHeight;
    camera.near = .1; camera.far = 100;
    camera.updateProjectionMatrix();
    renderer.render(scene, camera);
  }

  function line(points, color = 0x3b516c) {
    group.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), new THREE.LineBasicMaterial({ color })));
  }

  function label(text, x, y, z, color = '#eef3fa', scale = 1) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.font = '64px Roboto';
    const measured = Math.ceil(context.measureText(text).width);
    canvas.width = measured + 24; canvas.height = 100;
    context.font = '64px Roboto'; context.textAlign = 'center'; context.fillStyle = color;
    context.fillText(text, canvas.width / 2, 71);
    const texture = new THREE.CanvasTexture(canvas);
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, depthTest: false }));
    sprite.scale.set(canvas.width / 100 * .47 * scale, .47 * scale, 1);
    sprite.position.set(x, y, z);
    group.add(sprite);
  }

  function update(rows, key, selected, project) {
    for (const object of [...group.children]) {
      group.remove(object); object.geometry?.dispose();
      object.material?.map?.dispose(); object.material?.dispose();
    }
    objects = [];
    const maximum = maxima[key], heightScale = 4.1;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(10.8, 1.7), new THREE.MeshBasicMaterial({ color: 0x1b2d43, side: THREE.DoubleSide }));
    floor.rotation.x = -Math.PI / 2; floor.position.y = -.02;
    group.add(floor);
    for (let tick = 0; tick <= 2; tick++) {
      const y = tick * heightScale / 2;
      line([new THREE.Vector3(-4.9, y, -.75), new THREE.Vector3(4.9, y, -.75)]);
    }
    for (let day = 1; day <= data.study_days; day++) {
      const row = rows.find(item => item.day === day && item.project === project);
      const x = (day - 3.5) * 1.65;
      const active = Boolean(row);
      label('Day ' + day, x, -.45, .4, active ? '#eef3fa' : '#788da8', 1.2);
      if (!active) continue;
      const value = row[key], height = value / maximum * heightScale;
      if (value) {
        const chosen = selected?.day === day && selected?.project === project;
        const bar = new THREE.Mesh(new THREE.BoxGeometry(.94, height, .66), new THREE.MeshStandardMaterial({ color: chosen ? 0xefb45c : 0x699fe8, roughness: .85, metalness: 0 }));
        bar.position.set(x, height / 2, 0); bar.userData.row = row;
        group.add(bar); objects.push(bar);
      }
      const display = value >= 1e6 ? (value / 1e6).toFixed(1) + 'M' : value.toLocaleString('en-US');
      label(display, x, height + .3, .2, '#eef3fa', 1.4);
    }
    draw();
  }

  const ray = new THREE.Raycaster(), pointer = new THREE.Vector2();
  renderer.domElement.addEventListener('click', event => {
    const bounds = renderer.domElement.getBoundingClientRect();
    pointer.set((event.clientX - bounds.left) / bounds.width * 2 - 1, -(event.clientY - bounds.top) / bounds.height * 2 + 1);
    ray.setFromCamera(pointer, camera);
    const hit = ray.intersectObjects(objects)[0];
    if (hit) onSelect(hit.object.userData.row);
  });
  renderer.domElement.addEventListener('webglcontextlost', event => {
    event.preventDefault();
    document.getElementById('webglstatus').textContent = 'WebGL context lost. Exact values remain available in the project buttons and matrix.';
  });
  new ResizeObserver(draw).observe(container);
  return { update, camera(a, e) { azimuth = a; elevation = e; draw(); } };
}
