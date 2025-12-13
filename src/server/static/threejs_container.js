import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

let threejs_container, clock, mouthMixer, mixer, actions, activeAction, previousAction;
let camera, scene, renderer, model;

const api = { state: 'Idle' }

const API = {
    IDLE: "Idle",
    THINK: "Think",
    WAIT: "Wait",
    LISTEN: "Listen",
    TALK: "Talk",
    TELL: "Tell",
    YES: "Yes",
    NO: "No",
    ASK: "Ask"
};

init()

function init() {
    threejs_container = document.getElementById('threejs_container');
    const cw = threejs_container.getBoundingClientRect().width;
    const ch = threejs_container.getBoundingClientRect().height;

    camera = new THREE.PerspectiveCamera(50, cw / ch, 0.1, 10);
    camera.position.z = 1.5;
    camera.position.y = 1.6;

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x8ebfde);

    clock = new THREE.Clock();

    // lights

    scene.add(new THREE.AmbientLight(0xffffff, 1));
    const dir_light = new THREE.DirectionalLight(0xffffff, 2);
    dir_light.position.set(10, 10, 5);
    scene.add(dir_light);

    // model

    const loader = new GLTFLoader();
    loader.load('static/agent.glb', function (gltf) {

        model = gltf.scene;
        scene.add(model);
        setMouthMixer(model);
        createApi(model, gltf.animations);
        // const agent = model["children"][0];

    }, undefined, function (error) {
        console.error(error);
    });

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(cw, ch);
    renderer.setAnimationLoop(animate);
    threejs_container.appendChild(renderer.domElement);

}

function setMouthMixer(model) {
    const head = model.getObjectByName("head_1")
    const trackname = '.morphTargetInfluences[0]';
    const half_yap_sec = 0.2;

    const morphTrack = new THREE.NumberKeyframeTrack(trackname, [0, half_yap_sec, 2 * half_yap_sec], [0, 1, 0]);
    const clip = new THREE.AnimationClip('morph', -1, [morphTrack]);
    mouthMixer = new THREE.AnimationMixer(head);

    const action = mouthMixer.clipAction(clip);
    action.setLoop(THREE.LoopRepeat);
    action.play();
}

function createApi(model, animations) {
    const states = ['Idle', 'Think', 'Wait', 'Listen', 'Talk', 'Tell'];
    const emotes = ['Yes', 'No', 'Ask'];

    mixer = new THREE.AnimationMixer(model);

    actions = {};

    for (let i = 0; i < animations.length; i++) {

        const clip = animations[i];
        const action = mixer.clipAction(clip);
        actions[clip.name] = action;

        if (emotes.indexOf(clip.name) >= 0) {// || states.indexOf(clip.name) >= 2) {

            action.clampWhenFinished = true;
            action.loop = THREE.LoopOnce;

        }


    }

    const fade_sec = 0.5;

    // states

    for (let i = 0; i < states.length; i++) {
        const name = states[i];
        api[name] = function () {
            fadeToAction(name, fade_sec);
        }
    }

    // emotes

    function createEmoteCallback(name) {
        api[name] = function () {
            setTimeout(() => {
                fadeToAction(name, 0.2);
            }, 1000 * fade_sec);
            mixer.addEventListener('finished', restoreState);
        }
    }
    function restoreState() {
        mixer.removeEventListener('finished', restoreState);
        fadeToAction(api.state, 0.2);
    }

    for (let i = 0; i < emotes.length; i++) {
        createEmoteCallback(emotes[i])
    }

    // expressions 

    // finally

    activeAction = actions['Idle'];
    activeAction.play()
}

function fadeToAction(name, duration) {

    previousAction = activeAction;
    activeAction = actions[name];

    if (previousAction !== activeAction) {
        previousAction.fadeOut(duration);
    }

    playAction(activeAction, duration)
}

function playAction(action, duration) {
    action
        .reset()
        .setEffectiveTimeScale(1)
        .setEffectiveWeight(1)
        .fadeIn(duration)
        .play();
}

let play = false;
function animate() {

    const dt = clock.getDelta();
    if (mixer) mixer.update(dt);
    if (play) {
        mouthMixer.update(dt);
    }
    renderer.render(scene, camera);

}

function toggleMouth(new_state = API.TALK) {
    play = !play;
    mouthMixer.setTime(0);
    if (play) {
        api[new_state]();
    }
    else {
        api[API.IDLE]();
    }
}

export { toggleMouth, api as agentApi, API as AGENTAPI }