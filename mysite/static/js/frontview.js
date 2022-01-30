
const BACKGROUND_COLOR = 0xf1f1f1;

// Инициализируем сцену
const scene = new THREE.Scene();
// Установим цвет фона
    scene.background = new THREE.Color(BACKGROUND_COLOR );
    scene.fog = new THREE.Fog(BACKGROUND_COLOR, 6000, 9000);
const canvas = document.querySelector('#c');

// Инициализируем рендер
const renderer = new THREE.WebGLRenderer({canvas, antialias: true});
    renderer.shadowMap.enabled = true;
    renderer.setPixelRatio(window.devicePixelRatio); 

document.getElementById('divcanvas').appendChild(renderer.domElement);

m_width=mebelView['width'];
m_height=mebelView['height'];
m_depth=mebelView['depth'];
panels=mebelView['panels'];
materials=mebelView['materials'];
size=mebelView['size'];
//console.log(mebelView);

const sizeGroup = new THREE.Group();
addSize();
scene.add(sizeGroup)
sizeGroup.visible = false;
const INITIAL_MTL = new THREE.MeshPhongMaterial( {
     color: 0xeeeeee,
     shininess: 10 } );
//Создаю список материалов
const INITIAL_MAP =[]
materials.forEach(function(matAdd) {
    var texture = new THREE.TextureLoader().load(matAdd['map']);
        texture.wrapS=texture.wrapT=THREE.MirroredRepeatWrapping;
        texture.offset.set(0,0.5);
        texture.repeat.set(0.001,0.001);
        texture.center.set(.5, .5);
        texture.rotation=THREE.MathUtils.degToRad(0);
    var texture90 = new THREE.TextureLoader().load(matAdd['map']);
        texture90.wrapS=texture.wrapT=THREE.MirroredRepeatWrapping;
        texture90.offset.set(0,0.5);
        texture90.repeat.set(0.001,0.001);
        texture90.center.set(.5, .5);
        texture90.rotation=THREE.MathUtils.degToRad(90);
    var idtexture='0_'+matAdd['id']
    INITIAL_MAP[idtexture]=new THREE.MeshPhongMaterial( {
        //color:matAdd['color'],
        map: texture,
        //transparent:true,
        //opacity:0.5,
        //metalness:matAdd['metalness'],
        //roughness:matAdd['roughness']
    });
    idtexture='1_'+matAdd['id']
    INITIAL_MAP[idtexture]=new THREE.MeshPhongMaterial( {
        //color:matAdd['color'],
        map: texture90,
        //transparent:true,
        //opacity:0.5,
        //metalness:matAdd['metalness'],
        //roughness:matAdd['roughness']
    });
    idtexture='2_'+matAdd['id']
    INITIAL_MAP[idtexture]=new THREE.MeshPhongMaterial( {
        //color:matAdd['color'],
        map: texture,
        //transparent:true,
        //opacity:0.5,
        //metalness:matAdd['metalness'],
        //roughness:matAdd['roughness']
    });
    
});
//console.log(INITIAL_MAP)

const panelGroup = new THREE.Group();

panels.forEach(function(v) {
    const extrudeSettings = {
        steps: 1,
        depth: v['thickness'],
        material:0, //Цвет ДСП
        extrudeMaterial:1 //Цвет ПВХ
        };   
    contour=v['contour'];
    const shape = new THREE.Shape();
    contour.forEach(function(c){           
        if (c['type']=='1'){                 //T2DLine
            shape.moveTo( c['pos1x'],c['pos1y']);
            shape.lineTo( c['pos2x'],c['pos2y']);                
            }
        if (c['type']=='2'){          //T2DArc          
            shape.absarc(c['centerx'], c['centery'], c['radius'], c['startangle'],c['endangle'], !(c['arcdir']));
            }
        });
    
    const geometry = new THREE.ExtrudeGeometry( shape, extrudeSettings );
        geometry.normalizeNormals();
    py=v['posy']
    px=v['posx']
    pz=v['posz']
    quaternion = new THREE.Quaternion(v['rotx'], v['roty'], v['rotz'], v['rotw']);
    //console.log(v['texture']);
    /*
    texture.rotation = THREE.MathUtils.degToRad(0);
    if (v['texture']==1) {
        texture.rotation = THREE.MathUtils.degToRad(90);
        }
    */
    
    //const mesh = new THREE.Mesh( geometry, new THREE.MeshFaceMaterial([material,materialPVC]) ) ;
    NumMaterial=v['texture']+'_'+v['material']
    //PanelMaterial=materials.find(val => val.id === NumMaterial)
    //console.log(PanelMaterial.color)
    //INITIAL_MTL.color=PanelMaterial.color;
    const mesh = new THREE.Mesh( geometry, INITIAL_MAP[NumMaterial] ) ;
    //console.log(mesh.material.map.rotation);
    mesh.applyQuaternion(quaternion);
    mesh.position.set(px,py,pz);
    panelGroup.add( mesh );
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    //console.log(mesh);
    });

scene.add(panelGroup);

var hemiLight = new THREE.HemisphereLight( 0xffffff, 0xffffff, 0.61 );
    hemiLight.position.set( 0, 2700, 0 ); 
    scene.add( hemiLight );


// Поверхность пола
var floorGeometry = new THREE.PlaneGeometry(20000, 20000, 1, 1);
var floorMaterial = new THREE.MeshPhongMaterial({
    color: 0xeeeeee, // <------- здесь поменяли
    shininess: 0
    });
var floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.rotation.x = -0.5 * Math.PI;
    floor.receiveShadow = true;
    floor.position.y = -1;
    scene.add(floor);

var spotLight = new THREE.SpotLight(0xffffee);
    spotLight.position.set (m_width*1.3,m_height*1.3, m_depth*1.3); // позиция
    spotLight.castShadow = true; // создаем тень
    spotLight.penumbra=0.5;
    spotLight.shadow.camera.near = 2; // Проекция в магазин
    spotLight.shadow.camera.far = 20000; // проецируем дальнюю точку
    spotLight.shadow.camera.fov = 30; // Поле зрения проекции, угол прожектора
    spotLight.shadow.mapSize.width = 4096; // default
    spotLight.shadow.mapSize.height = 4096; // default
    //spotLight.target = floor; // Свет падает на землю
    spotLight.distance = 0; // Расстояние освещения, по умолчанию 0, что означает, что он может освещаться на бесконечностиspotLight.angle = 1; // угол освещения
    spotLight.intensity=0.8;
    scene.add(spotLight);





// добавляем камеру
var camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 100, 10000);    
    camera.position.x = m_width/2;
    camera.position.y = m_height*0.7;
    camera.position.z = m_depth*3;

var controls = new THREE.OrbitControls (camera, renderer.domElement);
    controls.target = new THREE.Vector3(m_width/2, m_height/2, 0);
    controls.maxPolarAngle = Math.PI / 2;
    controls.minPolarAngle = Math.PI / 3;
    controls.enableDamping = true;
    controls.enablePan = true;
    controls.dampingFactor = 0.1;
    controls.autoRotate = false; // Переключите это, если хотите, чтобы кресло автоматически поворачивалось 
    controls.autoRotateSpeed = 5; // 30









function addSize(){   
    const material = new THREE.LineBasicMaterial( { color: 0x0000ff } );
    size.forEach(function(v) {
        //contour=v['value'];
        px=v['posx'];
        py=v['posy'];
        pz=v['posz'];
        pl=v['length'];
        ps=v['size'];
        quaternion = new THREE.Quaternion(v['rotx'], v['roty'], v['rotz'], v['rotw']);
        const LinePoints = [];
        LinePoints.push(new THREE.Vector3(0,10,0));
        LinePoints.push(new THREE.Vector3(0,pl,0));
        LinePoints.push(new THREE.Vector3(0,pl-20,0));
        LinePoints.push(new THREE.Vector3(ps,pl-20,0));
        LinePoints.push(new THREE.Vector3(ps,pl,0));
        LinePoints.push(new THREE.Vector3(ps,10,0));
        const geometry = new THREE.BufferGeometry().setFromPoints( LinePoints );
        const line = new THREE.Line( geometry, material );
        line.applyQuaternion(quaternion);
        line.position.set(px,py,pz);
        sizeGroup.add( line );       
    });
}


function animate() {
    
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
    
    if (resizeRendererToDisplaySize(renderer)) {
      const canvas = renderer.domElement;
      camera.aspect = canvas.clientWidth / canvas.clientHeight;
      camera.updateProjectionMatrix();
    }
  }

function resizeRendererToDisplaySize(renderer) {
    const canvas = renderer.domElement;
    var width = window.innerWidth;
    var height = window.innerHeight;
    var canvasPixelWidth = canvas.width / window.devicePixelRatio;
    var canvasPixelHeight = canvas.height / window.devicePixelRatio;
    const needResize = canvasPixelWidth !== width || canvasPixelHeight !== height;
    if (needResize) {
      
      renderer.setSize(width, height, false);
    }
    return needResize;
  }


// Изменяем прозрачность всех пенелей
idTrans.onclick = function() {
    var allChildren = panelGroup.children;
    var length = allChildren.length;
   for(var i=0;i < length;i++) {
        allChildren[i].material.transparent=true;
        allChildren[i].material.opacity = 0.5;
        //allChildren[i].material.wireframe = true;
        
    }
  };

idWireFrame.onclick = function() {
    
    var allChildren = panelGroup.children;
    var length = allChildren.length;
   for(var i=0;i < length;i++) {
        allChildren[i].material.wireframe = true;
    }
  };

idTexture.onclick = function() {
    var allChildren = panelGroup.children;
    var length = allChildren.length;
   for(var i=0;i < length;i++) {
        allChildren[i].material.wireframe = false;
        allChildren[i].material.transparent=false;
        allChildren[i].material.opacity = 0.5;
    }
  };

function sizeCheck(){
    var chbox;
    chbox=document.getElementById('size');
        if (chbox.checked) {
            sizeGroup.visible = true;
        }
        else {
            sizeGroup.visible = false;
        }
    chbox=document.getElementById('fog');
        if (chbox.checked) {
            scene.fog.near = 6000;
            scene.fog.far = 9000;
        }
        else {
            scene.fog.near = 0.1;
            scene.fog.far = 0;
        }
    chbox=document.getElementById('light');
        if (chbox.checked) {
            spotLight.intensity=0.8;
        }
        else {
            spotLight.intensity=0;
        }
}

animate();