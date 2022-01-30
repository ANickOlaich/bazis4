var scene, renderer, camera;
var cube;
var controls;

init();
animate();

function init()
{
    const canvas = document.querySelector('#c');  
    const can = document.querySelector('#can');
    canvas.width=can.clientWidth-20;
    canvas.height=can.clientWidth-20;
    renderer = new THREE.WebGLRenderer({canvas});
    renderer.setClearColor( 0xEEEEEE );
    renderer.shadowMap.type = THREE.PCFShadowMap
    //renderer.shadowMap.enabled=true;    
    var width = canvas.width;
    var height = canvas.height;
    renderer.setSize (width, height);
    
    scene = new THREE.Scene();    
    console.log(mebelView);
    console.log(width)
    console.log(height)
    m_width=mebelView['width']
    m_height=mebelView['height']
    m_depth=mebelView['depth']
    panels=mebelView['panels']
    console.log(panels)
    var basicMaterial = new THREE.MeshBasicMaterial({color: 0x0095DD});
    panels.forEach(function(v) {
        const extrudeSettings = {
            steps: 1,
            depth: v['thickness'],
            material:0, //Цвет ДСП
            extrudeMaterial:1 //Цвет ПВХ
            };   
        contour=v['contour'];
        
        //Материал ДСП
        /*
        var texture = new THREE.TextureLoader().load('/static/materials/ph18113.jpg');
        texture.wrapS=texture.wrapT=THREE.MirroredRepeatWrapping;
        texture.offset.set(0,0.5);
        texture.repeat.set(0.001,0.001);
        texture.center.set(.5, .5);
        */
        const material = new THREE.MeshStandardMaterial({
          //color: 0xCCCCCC,
          side: THREE.DoubleSide,
          //map: texture // texture as a map for material
        }); 
        
        materialPVC=new THREE.MeshStandardMaterial({color: 0x777777}); //Материал ПВХ
        materialPVC.transparent=true;
        materialPVC.wireframe = false;
        //materialPVC.DoubleSide = true;
        
        const shape = new THREE.Shape();
        console.log('>>>'+v['title'])
        contour.forEach(function(c){           
            if (c['type']=='1'){                 //T2DLine
                console.log('Line')
                console.log('moveto('+c['pos1x']+','+c['pos1y']+')')
                shape.moveTo( c['pos1x'],c['pos1y']);
                console.log('lineto('+c['pos2x']+','+c['pos2y']+')')
                shape.lineTo( c['pos2x'],c['pos2y']);                
                }
            if (c['type']=='2'){          //T2DArc   
                console.log('Arc')             
               
                         
                shape.absarc(c['centerx'], c['centery'], c['radius'], c['startangle'],c['endangle'], (c['arcdir']));
                            
                }
                
            });
        
        const geometry = new THREE.ExtrudeGeometry( shape, extrudeSettings );
        geometry.normalizeNormals();
        py=v['posy']
        px=v['posx']
        pz=v['posz']
        quaternion = new THREE.Quaternion(v['rotx'], v['roty'], v['rotz'], v['rotw']);
        //geometry.applyQuaternion(quaternion);
        console.log(v['texture']);
        /*
        texture.rotation = THREE.MathUtils.degToRad(0);
        if (v['texture']==1) {
            texture.rotation = THREE.MathUtils.degToRad(90);
            }
        */
        
        //const mesh = new THREE.Mesh( geometry, new THREE.MeshFaceMaterial([material,materialPVC]) ) ;
        const mesh = new THREE.Mesh( geometry, materialPVC ) ;
        mesh.applyQuaternion(quaternion);
        mesh.position.set(px,py,pz);
        scene.add( mesh );
        });

    //Create a plane that receives shadows (but does not cast them)
    const planeGeometry = new THREE.PlaneGeometry( 1000, 1000, 32, 32 );
    const planeMaterial = new THREE.MeshStandardMaterial( { color: 0xEEEEEE } )
    const plane = new THREE.Mesh( planeGeometry, planeMaterial );
    plane.rotateX(4.71238898)
    plane.position.set(500,0,500);
    plane.receiveShadow = true;
    scene.add( plane );
    
    const light = new THREE.HemisphereLight( 0xffffbb, 0x080820, 0.5 );
    scene.add( light );
    
    var spotLight = new THREE.SpotLight(0xffffff);
    spotLight.position.set (m_width*1.3,3000, 3000); // позиция
    spotLight.castShadow = true; // создаем тень
    spotLight.penumbra=0.5;
    spotLight.shadow.camera.near = 2; // Проекция в магазин
    spotLight.shadow.camera.far = 20000; // проецируем дальнюю точку
    spotLight.shadow.camera.fov = 30; // Поле зрения проекции, угол прожектора
    spotLight.shadow.mapSize.width = 2048; // default
    spotLight.shadow.mapSize.height = 2048; // default
    spotLight.target = plane; // Свет падает на землю
    spotLight.distance = 0; // Расстояние освещения, по умолчанию 0, что означает, что он может освещаться на бесконечностиspotLight.angle = 1; // угол освещения
    scene.add(spotLight);
    
    const helper2 = new THREE.DirectionalLightHelper( spotLight, 500, 0x333333 );
    //scene.add( helper2 );
    

    var boxGeometry = new THREE.BoxGeometry(10, 10, 10);
    
    var cube = new THREE.Mesh(boxGeometry, basicMaterial);
    scene.add(cube);
    cube.rotation.set(0.4, 0.2, 0);
    camera = new THREE.PerspectiveCamera (45, width/height, 1, 400000);
    //camera = new THREE.PerspectiveCamera(70, width/height);
    //camera.position.z = 50;
    //scene.add(camera);
    camera.position.x = m_width*2;
    camera.position.y = m_height*0.7;
    camera.position.z = m_depth*8;
    
    //console.log(camera); 
    controls = new THREE.OrbitControls (camera, renderer.domElement);
    controls.target = new THREE.Vector3(m_width/4, m_height/4, 0);
    
}



function animate()
{
    //controls.update();
    requestAnimationFrame ( animate );  
    renderer.render (scene, camera);
}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }
/*
// Изменяем прозрачность всех пенелей
idTrans.onclick = function() {
    var allChildren = scene.children;
    var length = allChildren.length;
   for(var i=0;i < length;i++) {
        allChildren[i].material.transparent=true;
        allChildren[i].material.opacity = 0.5;
        //allChildren[i].material.wireframe = true;
        
    }
  };

//Изменяем цвет всех панелей на серый
idGray.onclick = function() {
    var cubeGeometry = new THREE.BoxGeometry (300,300,300);
    const material = new THREE.MeshStandardMaterial({  
  color: 0xDDDDDD
  });
    var allChildren = scene.children;
    var length = allChildren.length;
   for(var i=0;i < length;i++) {
        allChildren[i].material=material;
    }
  };

//Делаю снимок
idSnap.onclick=function() {

    // open in new window like this
    //
    var w = window.open('', '');
    w.document.title = "Screenshot";
    //w.document.body.style.backgroundColor = "red";
    var img = new Image();
    // Without 'preserveDrawingBuffer' set to true, we must render now
    renderer.render(scene, camera);
    }
    */