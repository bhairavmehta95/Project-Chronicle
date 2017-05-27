$(document).ready(function () {

	$( "input" ).keyup(function(e) {
		if (e.keyCode == 13) {
			enroll();
		}
	});

})

function enroll() {
	
	var postData = {
		classKey: $('#enrollInput').val()
	}

	$.ajax({
		type: 'POST',
		url: '/enroll/',
		data: postData,
		success: function(result) {
			window.location = "/classes/";
		},
		error: function() {
			alert("Sorry, we couldn't find that class. Please try a different class key or try again.");
		}
	});

}