let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let click_button = document.querySelector("#click-photo");
let canvas = document.querySelector("#canvas");


const url = location.protocol + '//' + location.host;
console.log(url);
var socket = io(url);

socket.on('connect', function(){
	console.log("Connected...!", socket.connected)
});

camera_button.addEventListener('click', async function() {
   	let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
	video.srcObject = stream;
});

click_button.addEventListener('click', function() {

	setInterval(function(){
		//code goes here that will be run every 5 seconds.
		canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

		canvas.toBlob(function(blob){
			let image = URL.createObjectURL(blob);
			handleimage(blob);
		},'image/png');
	}, 500);
});

async function handleimage(imageFile){
	console.log('originalFile instanceof Blob', imageFile instanceof Blob); // true
	console.log(`originalFile size ${imageFile.size / 1024} KB`);

	const options = {
		maxSizeMB: 0.025,
		maxWidthOrHeight: 720,
		useWebWorker: true
	}
	try {
		const compressedFile = await imageCompression(imageFile, options);
		console.log('compressedFile instanceof Blob', compressedFile instanceof Blob); // true
		console.log(`compressedFile size ${compressedFile.size / 1024 } KB`); // smaller than maxSizeMB

		// var imageUrl = await blobToBase64(imageFile)
		// document.querySelector("#image").src = imageUrl;
		await uploadserver(imageFile);
	} catch (error) {
		console.log(error);
	}
}

async function blobToBase64(blob) {
	return new Promise((resolve, _) => {
	  const reader = new FileReader();
	  reader.onloadend = () => resolve(reader.result);
	  reader.readAsDataURL(blob);
	});
  }

async function uploadserver(compressedFile){
	var form_data = new FormData();
	form_data.append('image', compressedFile)
	$.ajax({
		url: '/processing',
		type: 'POST',
		data: form_data,
		contentType: false,
		processData: false,
		success: function (response) {
			console.log(response);
			let image = document.querySelector("#image");
			image.src = response.Image;
		},
		error: function (response) {
			console.log(response);
		}
	});
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
}