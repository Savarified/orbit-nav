//import { render } from 'less';
import * as THREE from 'three';

const w = window.innerWidth;
const h = window.innerHeight;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, w/h, 0.1, 100);
camera.position.z = 5;
const renderer = new THREE.WebGLRenderer();
renderer.setSize(w, h);
document.body.appendChild(renderer.domElement);

const geometry = new THREE.SphereGeometry(1, 32, 32, 0, 2*Math.PI, 0, 2*Math.PI);
const material = new THREE.MeshBasicMaterial( { color: 0x00FF00 } ); 
const earth = new THREE.Mesh( geometry, material ); scene.add( earth );
const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444);
scene.add(hemiLight);
function animate(){
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

requestAnimationFrame(animate);