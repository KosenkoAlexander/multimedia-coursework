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

function sanity_check() {
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    cube.position.y = -1;
    scene.add(cube);
}
// sanity_check()

const loader = new GLTFLoader();
let mixer;
loader.load('static/LabX.glb', function (gltf) {
    let gl_scene = gltf.scene; scene.add(gl_scene); // console.log(gl_scene);
    const mesh = gl_scene["children"][0]; // console.log(mesh);
    // mesh['morphTargetInfluences']['0'] = 1;

    const trackname = '.morphTargetInfluences[0]';
    const half_yap_sec = 0.2;
    const morphTrack = new THREE.NumberKeyframeTrack(trackname, [0, half_yap_sec, 2 * half_yap_sec], [1, 0, 1]);
    const clip = new THREE.AnimationClip('morph', -1, [morphTrack]);
    mixer = new THREE.AnimationMixer(mesh);

    const action = mixer.clipAction(clip);

    action.setLoop(THREE.LoopRepeat);
    action.play();
    mixer.setTime(0);
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
const clock = new THREE.Clock();
function animate() {
    window.requestAnimationFrame(animate);
    if (play) {
        mixer.update(clock.getDelta());
    }
    renderer.render(scene, camera);
}
animate();

function toggle_play() {
    play = !play;
    if (!play) {
        mixer.setTime(0);
    }
}

export { toggle_play }