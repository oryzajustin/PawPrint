var bounds;
var coords;
var rectangle;
var url = "http://pawprint.dirt.io/cameras";
var camgrid = document.getElementById("cams");
var cameras;
var map;
var sendData;

$.getJSON(url, function(data) {
	cameras = data;
	placeMarkers();
});

function initMap() {
	map = new google.maps.Map(document.getElementById("map"), {
		center: {lat: 42.351, lng: -71.070},
		zoom: 14,
		streetViewControl: false
	});

	bounds = {
		north: 42.356,
		south: 42.346,
		east: -71.060,
		west: -71.080
	};
	coords = bounds;

	rectangle = new google.maps.Rectangle({
		bounds: bounds,
		editable: true,
		draggable: true
	});
	rectangle.setMap(map);

	rectangle.addListener("bounds_changed", updateView);

}

function placeMarkers() {
	console.log("Placing markers...");
	var markers = new Array(cameras.length);
	for (let i = 0; i < cameras.length; i++) {
		markers[i] = new google.maps.Marker({
			position: {lat: cameras[i].latitude, lng: cameras[i].longitude},
			map: map
		});
	}	
}

function formSubmit() {
	sendData = {
		cameraids: getCameras(coords),
		name: document.getElementById("name").value,
		phone: document.getElementById("phone").value,
		pet: document.getElementById("animal").value
	};
	$("#startBtn").addClass("is-loading");

	$.ajax({
	    type: "POST",
	    /*http://pawprint.dirt.io/request for success
	    http://dirt.io for error*/
	    url: "http://pawprint.dirt.io/request",
	    data: JSON.stringify(sendData),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data){
	    	window.location.replace("success.html");
	    },
	    error: function(errMsg) {
	    	$("#startBtn").removeClass("is-loading");
	        swal(
	        	'Error',
	        	errMsg.responseText,
	        	'error'
	        );
	    }
	});
}

function getCameras(coords) {
	var camID = [];
	for (let i = 0; i < cameras.length; i++) {
		if (cameras[i].longitude > coords.west && cameras[i].longitude < coords.east && cameras[i].latitude > coords.south && cameras[i].latitude < coords.north) {
			camID.push(cameras[i].id);
		}
	}
	return camID;
}

function updateView() {
	camgrid.innerHTML = "";
	coords = {
		north: rectangle.getBounds().getNorthEast().lat(),
		south: rectangle.getBounds().getSouthWest().lat(),
		east: rectangle.getBounds().getNorthEast().lng(),
		west: rectangle.getBounds().getSouthWest().lng(),
	}

	for (let i = 0; i < cameras.length; i++) {
		if (cameras[i].longitude > coords.west && cameras[i].longitude < coords.east && cameras[i].latitude > coords.south && cameras[i].latitude < coords.north) {
			camgrid.innerHTML += "<img class='innercam' src='"+ cameras[i].url +"'/><br>";
		}
	}
}
