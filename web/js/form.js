/*TODO
 *-replace URL in post request
 *
 */

var bounds;
var rectangle;
var url = "http://pawprint.dirt.io/cameras";
var form = document.getElementById("myForm");
var cameras;
var map;
var sendData;

$.getJSON(url, function(data) {
	cameras = data;
	delete data.latitude;
	delete data.longitude;
	placeMarkers();
});

function initMap() {
	map = new google.maps.Map(document.getElementById("map"), {
		center: {lat: 42.351, lng: -71.070},
		zoom: 14,
		streetViewControl: false
	});

	bounds = {
		north: 42.361,
		south: 42.341,
		east: -71.040,
		west: -71.100
	};

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
	let newBounds = {
		north: rectangle.getBounds().getNorthEast().lat(),
		south: rectangle.getBounds().getSouthWest().lat(),
		east: rectangle.getBounds().getNorthEast().lng(),
		west: rectangle.getBounds().getSouthWest().lng(),		
	}
	sendData = {
		cameraids: getCameras(newBounds),
		name: document.getElementById("name").value,
		phone: document.getElementById("phone").value,
		pet: document.getElementById("animal").value
	};
	sendData = JSON.stringify(sendData);
	$("#startBtn").addClass("is-loading");
	$.post( "https://mdislam.com", sendData, function( data ) {
	  console.log(data);
	  window.location.replace('success.html');
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