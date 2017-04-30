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
		var tile = $("<a></a>").addClass('tile').attr('href','/teacher/classPage/' + classArray[i].fields.class_key).data("classKey", classArray[i].fields.class_key);
		var key = $("<span></span>").addClass('class-key').text(classArray[i].fields.class_key);
		var banner = $("<div class='banner'></div>");
		var name = $("<span class='classNameSpan'></span>").text(classArray[i].fields.class_name).data("classKey", classArray[i].fields.class_key);
		var row1 = $("<div class='b-row1'></div>");
		var updateIcon = $("<i class='fa fa-pencil-square-o' data-toggle='tooltip' title='Edit'/>").data("classKey", classArray[i].fields.class_key);
		var deleteIcon = $("<i class='fa fa-times' data-toggle='tooltip' title='Delete'/>").data("classKey", classArray[i].fields.class_key);
		var iconContainer = $("<div class='icon-container'></div>");
		
		updateIcon.click(function(e) {
			e.preventDefault(); //stops the link from triggering
			openEditClassModal(this);
		})
		deleteIcon.click(function(e) {
			e.preventDefault(); //stops the link from triggering
			openConfirmDeleteModal(this);
		})
		row1.append(name);
		banner.append(row1);
		iconContainer.append(updateIcon, deleteIcon)
		tile.append(banner, key, iconContainer);
		$('.class-tiles').append(tile);
	}
	if ($('a.tile') == 0) {
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

function openEditClassModal(updateIcon) {
	var postData = {
		classKey: $(updateIcon).data().classKey
	}
	$.ajax({
		type: 'POST',
		url: 'ajax/getClass/',
		data: postData,
		success: function(result) {
			result = result[0].fields;
			$('.editClassName').val(result.class_name);
			$('.classKey').val(result.class_key);
			$('.numEnrollments').val(result.num_enrollments);
			$('#editClassModal').modal();
		}
	})
}

function postEditClass() {
	var postData = {
		classKey: $('.classKey').val(),
		className: $('.editClassName').val(),
	}
	var originalTile = $('a.tile:contains(' + postData.classKey + ')')
	$.ajax({
		type: 'POST',
		url: 'ajax/editClass/',
		data: postData,
		success: function(result) {
			$('#editClassModal').modal('toggle');
			$('.modal-backdrop').hide();
			originalTile.find('span.classNameSpan').text(postData.className);
		}
	})
}

function openConfirmDeleteModal(deleteIcon) {
	$('#deleteConfirmModal').modal();
	$('.hidden-delete-key').val($(deleteIcon).data().classKey);
}

function confirmDeleteClass() {
	if ($('#deleteConfirmModal input.confirm-txt').val() == "YES") {
		var postData = {
			classKey: $('.hidden-delete-key').val(),
		}
		$.ajax({
			type: 'POST',
			url: 'ajax/deleteClass/',
			data: postData,
			success: function(result) {
				$('#deleteConfirmModal').modal('toggle');
				$('.modal-backdrop').hide();
				$('a.tile:contains(' + postData.classKey + ')').remove()
			}
		})
	} else {
		$('#deleteConfirmModal input.confirm-txt').val('')
		$('#deleteConfirmModal').modal('toggle');
		$('.modal-backdrop').hide();
	}
}