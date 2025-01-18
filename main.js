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

const DEGREES_TO_RADIANS = 0.0174533;
function gcs_to_ecef(coordinate){
    let x = coordinate[0] * rad_conv;
    let y = coordinate[1] * rad_conv;
}

let system_total = [];
class Body { //celestial body class
    constructor(x,y,z,dx,dy,dz,mass,density,radius){
        this.x = x;
        this.y = y;
        this.z = z;
        this.dx = dx;
        this.dy = dy;
        this.dz = dz;
        this.mass = mass;
        this.density = density;
        this.radius = radius;
        system_total.push(this);
    }
}

class Spacecraft {
    constructor(x,y,z,dx,dy,dz,mass,height,radius){
        this.x = x;
        this.y = y;
        this.z = z;
        this.dx = dx;
        this.dy = dy;
        this.dz = dz;
        this.mass = mass;
        this.height = height;
        this.radius = radius;
    }
}
let launch_site = {
    longitude: 0,
    latitude: 0
};
let earth = new Body(0,0,0,0,0,0,123,123,123);
let ship123 = new Spacecraft(0,0,0,4/1000,0,0,123,123,123);
const sphereGeo = new THREE.SphereGeometry(1, 32, 32, 0, 2*Math.PI, 0, 2*Math.PI);
const cubeGeo = new THREE.BoxGeometry(1,1,1);
const earthMat = new THREE.MeshBasicMaterial( { color: 0x00FF00 } ); 
const earthObj = new THREE.Mesh(sphereGeo, earthMat); scene.add(earthObj);

const shipMat = new THREE.MeshBasicMaterial( {color: 0xFFFFFF });
const ship123Obj = new THREE.Mesh(cubeGeo, shipMat); scene.add(ship123Obj);
const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444);
scene.add(hemiLight);

function applyVelocities(){
    ship123.x += ship123.dx;
    ship123.y += ship123.dy;
    ship123.z += ship123.dz;
    ship123Obj.position.x = ship123.x;
    ship123Obj.position.y = ship123.y;
    ship123Obj.position.z = ship123.y;
}

function frame(){
    requestAnimationFrame(frame);
    applyVelocities();
    renderer.render(scene, camera);
}

requestAnimationFrame(frame);