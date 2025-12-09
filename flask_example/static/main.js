import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setAnimationLoop(animate);
document.body.appendChild(renderer.domElement);

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

scene.add(new THREE.AmbientLight(0xffffff, 1));
const dir_light = new THREE.DirectionalLight(0xffffff, 2);
dir_light.position.set(10, 10, 5);
scene.add(dir_light);

camera.position.z = 5;

function animate() {

    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    renderer.render(scene, camera);

}