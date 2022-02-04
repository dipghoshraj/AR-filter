const url = location.protocol + '//' + location.host;
const video = document.getElementById("videoElement");

video.width = 720;
video.height = 720;
var arintervals = null;
var imgintervals = null;

if (navigator.mediaDevices.getUserMedia) {
	navigator.mediaDevices.getUserMedia({ video: true })
	.then(function (stream) {
		video.srcObject = stream;
		video.play();
		updateVideo();
	})
	.catch(function (err0r) {
		console.log(err0r)
		console.log("Something went wrong!");
	});
}

function updateVideo(){
	imgintervals = setInterval(function(){
		const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
		canvas.getContext('2d').drawImage(video, 0, 0);

		var imagurl =  canvas.toDataURL('image/jpeg');
		console.log("adding still")
		let image = document.querySelector("#image");
		image.src = imagurl;
	}, 500);
}

function stopprocessing(){
	window.stop()
	if(imgintervals != null){
		clearInterval(imgintervals);
	}
	if (arintervals != null){
		clearInterval(arintervals);
	}
}

function onopencvReady(color){
	stopprocessing();
    arintervals = setInterval(function(){
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);

        canvas.toBlob(function(blob){
			handleimage(blob, color);
		},'image/png');

	}, 600);
}

async function handleimage(imageFile, color){
	// console.log('originalFile instanceof Blob', imageFile instanceof Blob); // true
	// console.log(`originalFile size ${imageFile.size / 1024} KB`);

	const options = {
		maxSizeMB: 0.025,
		maxWidthOrHeight: 720,
		useWebWorker: true
	}
	try {
		// const compressedFile = await imageCompression(imageFile, options);
		// console.log('compressedFile instanceof Blob', compressedFile instanceof Blob); // true
		// console.log(`compressedFile size ${compressedFile.size / 1024 } KB`); // smaller than maxSizeMB
		await uploadserver(imageFile,color);
	} catch (error) {
		console.log(error);
	}
}

async function uploadserver(compressedFile, color_value){
	var form_data = new FormData();
	console.log(color_value)
	form_data.append('image', compressedFile)
	$.ajax({
		url: '/processing',
		type: 'POST',
		data: form_data,
		contentType: false,
		headers: { 'color':  color_value},
		processData: false,
		success: function (response) {
			// console.log(response);
			let image = document.querySelector("#image");
			image.src = response.Image;

		},
		error: function (response) {
			console.log(response);
		}
	});
}

// 86, 0, 186, | 76, 66, 246|
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
}

async function send_packets(image_data, color){
	let color_value = hexToRgb(color);
	socket.emit('/api/v1/image', {imae_data: image_data, color_b: color_value.b, color_g: color_value.g, color_r: color_value.r});
}

async function get_packet(){
	socket.on('response_back', function(image){
        // console.log("get data")
		document.querySelector("#image").src = image;
    });
}