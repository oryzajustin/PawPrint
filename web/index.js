var bounds;
var rectangle;
var form = document.getElementById("myForm");

function initMap() {
	var map = new google.maps.Map(document.getElementById("map"), {
		center: {lat: 44.5452, lng: -78.5389},
		zoom: 9
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
}

function formSubmit() {
	//Post the newBounds
	var newBounds = {
		north: rectangle.getBounds().getNorthEast().lat(),
		south: rectangle.getBounds().getSouthWest().lat(),
		east: rectangle.getBounds().getNorthEast().lng(),
		west: rectangle.getBounds().getSouthWest().lng()
	};
	var print = "North lat: " +  newBounds.north
		+ "\nEast long: " + newBounds.east
		+ "\nSouth lat: " + newBounds.south
		+ "\nWest long: " + newBounds.west;
}
