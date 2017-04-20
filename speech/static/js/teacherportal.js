$(document).ready(function() {
	populateClasses();
})

function populateClasses() {
	$.ajax({
		type: 'GET',
		url: "getClasses/",
		success: function (result) {
			renderClasses(result);
		}
	})
}

function renderClasses(classArray) {
	for (var i = 0; i < classArray.length; i++) {
		var d = document;
		var tile = $("<a></a>").addClass('tile').attr('href','/teacher/classPage/' + classArray[i].fields.class_key);
		var key = $("<span></span>").addClass('class-key').text(classArray[i].fields.class_key);
		var banner = $("<div></div>");
		var name = $("<span></span>").text(classArray[i].fields.class_name);
		banner.append(name);
		tile.append(banner);
		tile.append(key);
		$('.class-tiles').append(tile);
	}
	if (classArray.length == 0) {
		var message = $("<div class='no-class-message'>It seems you do not have any classes. Click the Add Class button to create a new class...</div>");
		$('.class-tiles').append(message);
	} else {
		$('.no-class-message').remove();
	}
}

function addClass() {
	var postData = {
		className: $('#className').val()
	}
	$.ajax({
		type: 'POST',
		url: 'createClass/',
		data: postData,
		success: function(result) {
			renderClasses($.parseJSON(result));
			$('#myModal').modal('toggle');
			$('.modal-backdrop').hide();
		}
	})
}
