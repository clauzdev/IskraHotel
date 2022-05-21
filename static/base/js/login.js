(async function() {
  var width = 320;    // We will scale the photo width to this
  var height = 180;     // This will be computed based on the input stream

  var streaming = false;


  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;
  var inp = null;
  var username = document.getElementById('username');
  var photo_exists = document.getElementById('photo_exists');
  const photoBlock = document.getElementById('photoBlock');
  const login_button = document.getElementById('loginButton');
  const myForm = document.getElementById('contactForm');
  
  function endup() {
	video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');
	inp = document.getElementById('webimg');
	photo_exists = document.getElementById('photo_exists');
	
	navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.pause();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });
	
	video.removeEventListener('canplay', function(ev){
      if (!streaming) {
        height = 180; //video.videoHeight / (video.videoWidth/width);
      
        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.
      
        if (isNaN(height)) {
          height = width / (16/9);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    });
	login_button.removeEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
	  video.pause();
	  restartbutton.style.display = "block";
	  startbutton.style.display = "none";
	  myForm.submit();
    }, false);
	login_button.addEventListener('click', function(ev){
	  myForm.submit();
    }, false);
	clearphoto();	
  }
  
  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');
	restartbutton = document.getElementById('restartbutton');
	inp = document.getElementById('webimg');
	photo_exists = document.getElementById('photo_exists');

    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = 180;
      
        if (isNaN(height)) {
          height = width / (16/9);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);

    startbutton.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
	  video.pause();
	  restartbutton.style.display = "block";
	  startbutton.style.display = "none";
    }, false);
    
	restartbutton.addEventListener('click', function(ev){
	  video.play();
	  restartbutton.style.display = "none";
	  startbutton.style.display = "block";
    }, false);
	
	login_button.removeEventListener('click', function(ev){
	  myForm.submit();
    }, false);
	
	login_button.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
	  video.pause();
	  restartbutton.style.display = "block";
	  startbutton.style.display = "none";
	  myForm.submit();
    }, false);
	
    clearphoto();
  }

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
	inp.setAttribute('value', data);
  }

  function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);
    
      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
	  inp.setAttribute('value', data);
    } else {
      clearphoto();
    }
  }

  var username = document.getElementById('username');
  var photo_exists = document.getElementById('photo_exists');
  var initSqlJs = window.initSqlJs;
  const SQL = await initSqlJs({
    locateFile: file => `https://sql.js.org/dist/${file}`
  });
  //const fetched = await fetch("../../root/db.sqlite3");
  const buf = await fetech("../../root/db.sqlite3");//new ArrayBuffer(fetched);
  console.log("BUFFER" + buf);
  var db = new SQL.Database(new Uint8Array(buf));
  var contents = null;
  var contentik = null;
  username.addEventListener('input', function() {
	  contents = db.exec("select photo from customer_customer where user_id = (select id from authentication_user where username = '"+ username.value + "')");
    try {
      contentik = contents[0].values[0][0]
    } catch (error) {
      contentik = ""
    }
	  console.log(contentik);
	  if (contentik != "") {
		photoBlock.style.display="block";
		startup();
	  } else {
		photoBlock.style.display="none";
		endup();
	  }
  });
  async function fetech(url) {
    const response = await fetch(url);
    return response.arrayBuffer();
  }
})();
