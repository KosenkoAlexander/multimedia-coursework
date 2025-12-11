import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const threejs_container = document.getElementById('threejs_container');
const cw = threejs_container.getBoundingClientRect().width;
const ch = threejs_container.getBoundingClientRect().height;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, cw / ch, 0.1, 10);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(cw, ch);
threejs_container.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
cube.position.y = -1;
scene.add(cube);

const loader = new GLTFLoader();
let ladybug;
loader.load('static/scene.gltf', function (gltf) {
    ladybug = gltf.scene; ladybug.scale.set(50, 50, 50); ladybug.rotation.x = 1; scene.add(ladybug);
},
    undefined, function (error) { console.error(error); }
);

scene.background = new THREE.Color(0x8ebfde);
scene.add(new THREE.AmbientLight(0xffffff, 1));
const dir_light = new THREE.DirectionalLight(0xffffff, 2);
dir_light.position.set(10, 10, 5);
scene.add(dir_light);

camera.position.z = 5;

let play = false;
function animate() {
    window.requestAnimationFrame(animate);
    if (play) {
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
    }
    renderer.render(scene, camera);
}
animate();

function toggle_play() {
    play = !play;
}

export { toggle_play }