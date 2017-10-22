var bounds;
var rectangle;
var url = "http://pawprint.dirt.io/cameras";
var form = document.getElementById("myForm");
var coordDiv = document.getElementById("mapText");
var cameras;
var map;
var sendData;

$.getJSON(url, function(data) {
	console.log('cameras load')
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
	//Post the newBounds
	var nameValue = document.getElementById("name").value;
	var phoneValue = document.getElementById("phone").value;
	var petValue = document.getElementById("animal").value;

	console.log(nameValue + " " + phoneValue + " " + petValue);
	let newBounds = {
		north: rectangle.getBounds().getNorthEast().lat(),
		south: rectangle.getBounds().getSouthWest().lat(),
		east: rectangle.getBounds().getNorthEast().lng(),
		west: rectangle.getBounds().getSouthWest().lng()
	};
	let print = "North lat: " +  newBounds.north
		+ "\nEast long: " + newBounds.east
		+ "\nSouth lat: " + newBounds.south
		+ "\nWest long: " + newBounds.west;
	console.log(print);
}

function updateView() {
	let newBounds = {
		north: rectangle.getBounds().getNorthEast().lat(),
		south: rectangle.getBounds().getSouthWest().lat(),
		east: rectangle.getBounds().getNorthEast().lng(),
		west: rectangle.getBounds().getSouthWest().lng()
	};

	let print = "Box is around: ";
	for (let i = 0; i < cameras.length; i++) {
		if (cameras[i].longitude > newBounds.west && cameras[i].longitude < newBounds.east && cameras[i].latitude > newBounds.south && cameras[i].latitude < newBounds.north) {
			print += " " + cameras[i].id;
		}
	}
	coordDiv.innerHTML = print;	
}

