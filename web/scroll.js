$(document).ready(function() {
	$("#mybtn").click(function() {
		$("html, body").animate({
			scrollTop: $("#myForm").offset().top},
			"slow");
	})
});