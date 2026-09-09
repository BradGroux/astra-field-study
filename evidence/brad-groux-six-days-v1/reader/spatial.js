import * as THREE from './vendor/three.module.js';
export async function createSpatial(container,data,onSelect){
 const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0xe5e9e2);container.appendChild(renderer.domElement);
 const scene=new THREE.Scene(),camera=new THREE.OrthographicCamera(),group=new THREE.Group();scene.add(group);scene.add(new THREE.AmbientLight(0xffffff,2));const sun=new THREE.DirectionalLight(0xffffff,3);sun.position.set(8,18,10);scene.add(sun);
 const projects=[...new Set(data.rows.map(x=>x.project))],maxima=Object.fromEntries(['responses','total_tokens','corrective_units'].map(k=>[k,Math.max(1,...data.rows.map(x=>x[k]))]));
 let az=25,el=46,objects=[],selected=null;
 function draw(){const w=container.clientWidth,h=container.clientHeight;renderer.setSize(w,h,false);const aspect=w/h,span=Math.max(16,18/aspect);camera.left=-span*aspect/2;camera.right=span*aspect/2;camera.top=span/2;camera.bottom=-span/2;camera.near=.1;camera.far=200;const a=az*Math.PI/180,e=el*Math.PI/180;camera.position.set(32*Math.sin(a)*Math.cos(e),32*Math.sin(e),32*Math.cos(a)*Math.cos(e));camera.lookAt(0,1,0);camera.updateProjectionMatrix();renderer.render(scene,camera)}
 function label(text,x,y,z,size=1.3){const c=document.createElement('canvas');c.width=512;c.height=128;const cx=c.getContext('2d');cx.font='80px system-ui';cx.textAlign='center';cx.fillStyle='#173d46';cx.fillText(text,256,92);const map=new THREE.CanvasTexture(c),sprite=new THREE.Sprite(new THREE.SpriteMaterial({map,depthTest:false}));sprite.scale.set(size,size*128/512,1);sprite.position.set(x,y,z);group.add(sprite)}
 function update(rows,key,sel){selected=sel;while(group.children.length){const o=group.children[0];group.remove(o);o.geometry?.dispose();if(o.material){o.material.map?.dispose();o.material.dispose()}}objects=[];
 const max=maxima[key],height=5.8,active=new Set(rows.map(x=>x.day+'|'+x.project));
 const grid=new THREE.GridHelper(13,18,0xafbcb4,0xc4cec5);grid.scale.x=.68;group.add(grid);
 for(let d=1;d<=6;d++)label('Day '+d,(d-3.5)*1.35,.05,7.05,1.3);
 projects.forEach((p,i)=>label(p,-5.55,.1,(i-8.5)*.72,2.1));
 for(let i=0;i<=4;i++){const y=i*height/4;label(Math.round(max*i/4).toLocaleString('en-US'),4.75,y,6.8,1.8);const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(4.35,y,6.4),new THREE.Vector3(4.5,y,6.4)]),new THREE.LineBasicMaterial({color:0x597776}));group.add(line)}
 const axis=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(4.35,0,6.4),new THREE.Vector3(4.35,height,6.4)]),new THREE.LineBasicMaterial({color:0x597776}));group.add(axis);
 for(const x of data.rows){if(!active.has(x.day+'|'+x.project)||!x[key])continue;const h=x[key]/max*height;const chosen=sel&&x.day===sel.day&&x.project===sel.project;const bar=new THREE.Mesh(new THREE.BoxGeometry(.84,h,.49),new THREE.MeshStandardMaterial({color:chosen?0xb56538:key==='corrective_units'?0x9c582f:0x27858a,roughness:1,metalness:0}));bar.position.set((x.day-3.5)*1.35,h/2,(projects.indexOf(x.project)-8.5)*.72);bar.userData.row=x;group.add(bar);objects.push(bar)}draw();
 }
 const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();renderer.domElement.addEventListener('click',e=>{const b=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-b.left)/b.width*2-1,-(e.clientY-b.top)/b.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(objects)[0];if(hit)onSelect(hit.object.userData.row)});
 renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();container.nextElementSibling.textContent='WebGL context lost. Use the complete flat matrix below.'});new ResizeObserver(draw).observe(container);
 return {update,camera(a,e){az=a;el=e;draw()}};
}
