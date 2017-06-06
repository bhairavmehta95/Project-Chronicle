$(document).ready(function() {
	populateClasses();
	$('.ui.accordion').accordion();
})

/* MENU */
function addClassToMenu(className) {
	$activeItem = $('#mainMenu .item.active');
	$newItem = $activeItem.clone();
	$activeItem.removeClass('active');
	$newItem.find('span').text(className);
	$newItem.find('i').remove();
	$newItem
		.addClass('class-item')
		.appendTo('#mainMenu .left.menu');
	$('#mainMenu .right.menu .item.addClass').hide();
	$('#mainMenu .right.menu .item.addTopic').show();
}

function removeClassFromMenu() {
	menuItem = $('#mainMenu .item.class-item')
	menuItem.remove();
}


/* CLASSES */
function showHomeDetails() {
	$('#topicContainer').hide();
	$('#topicContainer').find('.accordion-row:not(.template)').remove();
	$('#classContainer').show();
	removeClassFromMenu();
}

function populateClasses() {
	$.ajax({
		type: 'GET',
		url: "/teacher/getClasses/",
		success: function (results) {
			results.forEach(function (myClass) {
				var data = myClass.fields;
				renderClass(data);
			})
		}
	})
}

function addClass(name) {
	var postData = {
		className: name
	}
	$.ajax({
		type: 'POST',
		url: '/teacher/createClass/',
		data: postData,
		success: function(result) {
			data = $.parseJSON(result)[0].fields;
			renderClass(data, true);
		}
	})
}

function deleteClass(classKey) {
	var postData = {
		classKey: classKey
	}
	$.ajax({
			type: 'POST',
			url: '/teacher/ajax/deleteClass/',
			data: postData,
			success: function(result) {
				$('.card:contains(' + classKey + ')').remove()
			}
		})
}

function editClass(name, classKey) {
	var postData = {
		classKey: classKey,
		className: name,
	}
	var originalTile = $('.card:contains(' + classKey + ')');
	$.ajax({
		type: 'POST',
		url: '/teacher/ajax/editClass/',
		data: postData,
		success: function(result) {
			originalTile.find('.content .header').text(name);
		}
	})
}

function renderClass(data, atFront) {
	var newCard = $('#classContainer .card.template').clone();
	newCard.data(data)
	newCard.find('.header').text(data.class_name);
	newCard.find('.enrollments-count').text(data.num_enrollments);
	newCard.find('.class-key').text(data.class_key);
	newCard.find('.menu .detail.item').click(function() {
		var $classCard = $(this).closest('.card');
		showClassDetails($classCard.data().class_key);
		addClassToMenu($classCard.data().class_name)
	});
	newCard.find('.menu .edit.item').click(function() {
		openModal('editClassModal', this);
	});
	newCard.find('.menu .delete.item').click(function() {
		openModal('confirmDeleteClassModal', this);
	});
	newCard.removeClass('template')
	if (atFront) {
		newCard.prependTo('#classContainer');
	} else {
		newCard.appendTo('#classContainer');
	}
}


/* TOPICS */
function showClassDetails(classKey) {
	$('#classContainer').hide();
	$('#topicContainer').show();
	$('#classKey').val(classKey)
	populateTopics(classKey);
}

function populateTopics(classKey) {
	$.ajax({
		type: 'GET',
		url: '/teacher/gettopics/' + classKey + '/',
		success: function (results) {
			results.forEach(function (topic) {
				var data = topic.fields;
				data.topic_id = topic.pk
				renderTopic(data);
			})
		}
	})
}

function addTopic(topicName) {
	var postData = {
		topicName: topicName,
		classKey: $('#classKey').val()
	}
	$.ajax({
		type: 'POST',
		url: '/teacher/addtopic/',
		data: postData,
		success: function(result) {
			data = $.parseJSON(result)[0].fields;
			data.topic_id = $.parseJSON(result)[0].pk;
			renderTopic(data);
		}
	})
}

function renderTopic(topicData) {
	$accordionRow = $('.accordion-row.template').clone();
	$accordionRow.find('.title span').text(topicData.topic_name);
	$accordionRow
		.removeClass('template')
		.data(topicData)
		.appendTo('#topicContainer');
}

function editTopic(name, topicId) {
	originalTile = $('#topicContainer .accordion-row:not(.template)').filter(function() {
		return ($(this).data().topic_id == topicId)
	})
	postData = {
		topicId: topicId,
		topicName: name
	}
	$.ajax({
		type: 'POST',
		url: '/teacher/ajax/editTopic/',
		data: postData,
		success: function(result) {
			originalTile.find('.title span').text(name);
		}
	})
}

function deleteTopic(topicId) {
	var postData = {
		topicId: topicId
	}
	$.ajax({
		type: 'POST',
		url: '/teacher/ajax/deleteTopic/',
		data: postData,
		success: function(result) {
			$('#topicContainer .accordion-row:not(.template)').each(function() {
				if ($(this).data().topic_id == topicId) {
					$(this).remove();
				}
			})
		}
	})
}


/* MODALS */
function openModal(modalName, trigger) {
	switch (modalName) {

		case 'addClass':
			$('#classModal .header').text('Add A Class');
			$('#classModal .button.approve').text('Create');
			$('#newClassName').val('');
			$('#classModal')
				.modal({
					onApprove : function() {
			  			submitModal('addClass');
			  		}
				})
				.modal('show');
			break;

		case 'confirmDeleteClassModal':
			var $classCard = $(trigger).closest('.card');
			$('#confirmModal')
				.modal({
					onApprove : function() {
			  			submitModal('deleteClass');
			  		}
				})
				.modal('show');
			$('#confirmModal .hidden-id').val($classCard.data().class_key);
			break;

		case 'editClassModal':
			$('#classModal .header').text('Edit Class');
			$('#classModal .button.approve').text('Edit');
			var $classCard = $(trigger).closest('.card');
			$('#newClassName').val($classCard.data().class_name);
			$('#classModal .hidden-id').val($classCard.data().class_key);
			$('#classModal')
				.modal({
					onApprove: function() {
						submitModal('editClass')
					}
				})
				.modal('show');
			break;

		case 'addTopic':
			$('#topicModal .header').text('Add Topic');
			$('#topicModal .button.approve').text('Create');
			$('#topicNameField').val('');
			$('#topicModal')
				.modal({
					onApprove : function() {
			  			submitModal('addTopic');
			  		}
				})
				.modal('show');
			break;

		case 'editTopic':
			var $accordionRow = $(trigger).closest('.accordion-row');
			$('#topicModal .header').text('Edit Topic');
			$('#topicModal .button.approve').text('Save');
			$('#topicNameField').val($accordionRow.data().topic_name);
			$('#topicModal .hidden-id').val($accordionRow.data().topic_id);
			$('#topicModal')
				.modal({
					onApprove : function() {
			  			submitModal('editTopic');
			  		}
				})
				.modal('show');
			break;

		case 'confirmDeleteTopic':
			var $accordionRow = $(trigger).closest('.accordion-row');
			$('#confirmModal')
				.modal({
					onApprove : function() {
			  			submitModal('deleteTopic');
			  		}
				})
				.modal('show');
			$('#confirmModal .hidden-id').val($accordionRow.data().topic_id);
			break;
	}
}

function submitModal(modalAction) {
	switch (modalAction) {
		case 'addClass':
			name = $('#newClassName').val();
			addClass(name);
			break;
		case 'deleteClass':
			classKey = $('#confirmModal .hidden-id').val();
			deleteClass(classKey);
			break;
		case 'editClass':
			name = $('#newClassName').val();
			classKey = $('#classModal .hidden-id').val();
			editClass(name, classKey);
			break;
		case 'addTopic':
			name = $('#topicNameField').val();
			addTopic(name);
			break;
		case 'editTopic':
			name = $('#topicNameField').val();
			topicId = $('#topicModal .hidden-id').val();
			editTopic(name, topicId);
			break;
		case 'deleteTopic':
			topicId = $('#confirmModal .hidden-id').val();
			deleteTopic(topicId);
			break;
	}
}
