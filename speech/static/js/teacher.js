$(document).ready(function() {
	populateClasses();
	$('.ui.accordion').accordion();
})

/* MENU */
function addClassToMenu(className) {
	$('#mainMenu .item.active').removeClass('active');;
	$templateItem = $('#mainMenu .item.template')
	$newItem = $templateItem.clone();
	$newItem.find('span').text(className);
	$newItem
		.addClass('class-item active')
		.removeClass('template')
		.appendTo('#mainMenu .left.menu')
		.click(function () {
			showClassDetails($('#classKey').val(), $('#classId').val());
			$(this).addClass('active')
			$(this).nextAll().remove();
			setRightMenu('addTopic');
		});
	setRightMenu('addTopic');
}

function addNewQuestionToMenu() {
	$activeItem = $('#mainMenu .item.active');
	$newItem = $activeItem.clone();
	$activeItem.removeClass('active');
	$newItem.find('span').text('New Question');
	$newItem.find('i').remove();
	$newItem
		.addClass('question-item')
		.appendTo('#mainMenu .left.menu');
	setRightMenu();
}

function removeClassFromMenu() {
	$('#mainMenu .item.class-item').remove();
	$('#mainMenu .item.home').addClass('active');
	setRightMenu('addClass');
}

function setRightMenu(setting) {
	$('#mainMenu .right.menu .item').hide();
	if (setting) {
		$('#mainMenu .right.menu .item.' + setting).show();
	}
}


/* CLASSES */
function showHomeDetails() {
	closeHideablesExcept('classContainer');
	removeClassFromMenu();
}

function populateClasses() {
	$.ajax({
		type: 'GET',
		url: "/teacher/getClasses/",
		success: function (results) {
			results.forEach(function (myClass) {
				var data = myClass.fields;
				data.class_id =  myClass.pk;
				renderClass(data);
			})
			toggleMessage('noClasses');
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
			data.class_id =  $.parseJSON(result)[0].pk;
			renderClass(data, true);
			toggleMessage('noClasses');
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
				$('.card:contains(' + classKey + ')').remove();
				toggleMessage('noClasses');
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
		showClassDetails($classCard.data().class_key, $classCard.data().class_id);
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
function showClassDetails(classKey, classId) {
	closeHideablesExcept('topicContainer');
	$('#classKey').val(classKey);
	$('#classId').val(classId);
	populateTopics(classKey);
}

function populateTopics(classKey) {
	$.ajax({
		type: 'GET',
		url: '/teacher/gettopics/' + classKey + '/',
		success: function (results) {
			results.forEach(function (topic) {
				var data = topic.fields;
				data.topic_id = topic.pk;
				renderTopic(data);
			})
			toggleMessage('noTopics');
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
			toggleMessage('noTopics');
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
	populateQuestions($accordionRow, topicData);
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
			toggleMessage('noTopics');
		}
	})
}


/* Questions */
function populateQuestions($accordionRow, topicData) {
	postData = {
		topicId: topicData.topic_id
	}
	$.ajax({
		type: 'POST',
		url: '/teacher/ajax/getQuestionsInTopic/',
		data: postData,
		success: function(results) {
			results.forEach(function (question) {
				var data = question.fields;
				data.question_id = question.pk;
				renderQuestion($accordionRow, data);
			})
			toggleMessage('noQuestions', $accordionRow);
		}
	});
}

function renderQuestion($accordionRow, questionData) {
	var newQuestion = $accordionRow.find('.segment.question.template').clone();
	var contentArea = $accordionRow.find('.question.segments')
	newQuestion.find('span').text(questionData.question_title);
	newQuestion
		.data(questionData)
		.removeClass('template')
		.appendTo(contentArea);
}

function openNewQuestionBuilder(trigger) {
	var topicId = $(trigger).closest('.accordion-row').data().topic_id
	window.location = '/builder/' + $('#classId').val() + '/' + topicId
	// console.log($(trigger).closest('.accordion-row').data().topic_id)
	// $('#topicId').val($(trigger).closest('.accordion-row').data().topic_id)
	// addNewQuestionToMenu();
	// closeHideablesExcept('questionContainer');
}

function goToBuilder(trigger) {
	var data = $(trigger).data()
	window.location = '/builder/' + $('#classId').val() + '/' + data.topic_id + '/' + data.question_id
}

function submitQuestion() {
	alert($('#classId').val())
	postData = {
		classId: $('#classId').val(),
		topicId: $('#topicId').val(),
		sources: $('#id_sources').val(),
		questionTitle: $('#id_question_title').val(),
		numKeywords: $('#id_keywords_to_return').val()
	}
	$.ajax({
		type: 'POST',
		url: '/buildNewQuestion/',
		data: postData,
		success: function(results) {
			alert("Reed, you did it!");
		}
	});
}


/* GENERAL */
function closeHideablesExcept(hideableID) {
	$('.hideable').hide();
	if (hideableID != 'topicConainer') {
		$('#topicContainer').find('.accordion-row:not(.template)').remove();
	}
	$('#' + hideableID).show();
}

function toggleMessage(message, $container) {
	switch(message) {
		case 'noClasses':
			if (!$('#classContainer .card:not(.template)').length) {
				$('#noClassesMessage').show();
			} else {
				$('#noClassesMessage').hide();
			}
			break;
		case 'noTopics':
			if (!$('#topicContainer .accordion-row:not(.template)').length) {
				$('#noTopicsMessage').show();
			} else {
				$('#noTopicsMessage').hide();
			}
			break;
		case 'noQuestions':
			if (!$container.find('.question.segment:not(.template)').length) {
				$container.find('.noQuestionsMessage').show();
			} else {
				$container.find('.noQuestionsMessage').hide();
			}
			break;
	}
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
