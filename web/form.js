var bounds;
var rectangle;
var form = document.getElementById("myForm");
var coordDiv = document.getElementById("mapText");
var camera1 = {lat: 44.502, lng: -78.500, desc: "test"};
var camera2 = {lat: 44.610, lng: -78.300, desc: "camera2"};
var cameras = new Array(camera1, camera2);


function initMap() {
	var map = new google.maps.Map(document.getElementById("map"), {
		center: {lat: 44.5452, lng: -78.5389},
		zoom: 9,
		streetViewControl: false
	});

	bounds = {
		north: 44.599,
		south: 44.490,
		east: -78.443,
		west: -78.649
	};

	rectangle = new google.maps.Rectangle({
		bounds: bounds,
		editable: true,
		draggable: true
	});
	rectangle.setMap(map);
	var markers = new Array(cameras.length);
	for (let i = 0; i < cameras.length; i++) {
		markers[i] = new google.maps.Marker({
			position: cameras[i],
			map: map
		});
	}
	/*
	var marker = new google.maps.Marker({
		position: camera1,
		map: map
	});
	*/
	rectangle.addListener("bounds_changed", updateView);

}

function formSubmit() {
	//Post the newBounds
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
		if (cameras[i].lng > newBounds.west && cameras[i].lng < newBounds.east && cameras[i].lat > newBounds.south && cameras[i].lat < newBounds.north) {
			print += " " + cameras[i].desc;
		}
	}
	coordDiv.innerHTML = print;	
}

