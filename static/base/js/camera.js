(function() {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.

  var width = 480;    // We will scale the photo width to this
  var height = 270;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  var streaming = false;

  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.

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
	
	loginButton.
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
        height = video.videoHeight / (video.videoWidth/width);
      
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
	defaultloginbutton();
	clearphoto();	
  }
  function defaultloginbutton() {
	login_button.addEventListener('click', function(ev){
		console.log('idi naxyi')
	  myForm.submit();
    }, false);
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
        height = 270; //video.videoHeight / (video.videoWidth/width);
      
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
	
  // Fill the photo with an indication that none has been
  // captured.

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
	inp.setAttribute('value', data);
  }
  
  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a PNG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.

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

  // Set up our event listener to run the startup process
  // once loading is complete.
  document.addEventListener("DOMContentLoaded", defaultloginbutton());
  photo_exists.addEventListener('change', function() {
	  if (this.checked) {
		photoBlock.style.display="block";
		startup();
	  } else {
		photoBlock.style.display="none";
		endup();
	  }
  });
})();