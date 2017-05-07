$(document).ready(function() {
	populateTopics();
	//populateStudents();
})

function populateTopics() {
	$.ajax({
		type: 'GET',
		url: "/teacher/gettopics/" + $('#classKey').val(),
		success: function (result) {
			renderTopics(result);
		}
	})
}

function populateStudents() {
	var postData = {
		classKey: $('#classKey').val()
	}
	$.ajax({
		type: 'POST',
		url: "/teacher/ajax/getStudentsInClass/",
		data: postData,
		success: function (result) {
			renderStudents(result);
		}
	})
}

function addTopic() {
	var postData = {
		topicName: $('#topicName').val(),
		classKey: $('#classKey').val(),
		classId: $('#classId').val()
	}
	console.log(postData);
	$.ajax({
		type: 'POST',
		url: '/teacher/addtopic/',
		data: postData,
		success: function(result) {
			renderTopics($.parseJSON(result));
			$('#myModal').modal('toggle');
			$('.modal-backdrop').hide();
		}
	})
}

function renderTopics(topicArray) {
	for (var i = 0; i < topicArray.length; i++) {	
		var d = document;
		var link = $("<div class='topic-link'></div>")
			.attr("topicNumber", topicArray[i].pk);
		var name = $("<span></span>").text(topicArray[i].fields.topic_name);
		var downArrow = $("<i class='fa fa-chevron-down'> </i>");
		var plusIcon = $("<i onclick='questionBuilderModal.open(this)' class='fa fa-plus-square-o'> </i>");
		var editIcon = $("<i onclick='openEditTopicModal(this)' class='fa fa-edit'> </i>");
		
		link.append(name, editIcon, plusIcon, downArrow);
		$('.question-panel').append(link);
	}
}

var questionBuilderModal = {
	topic: '',
	open: function(topic) {
		this.topic = topic.getAttribute('topicNumber');
		$('#questionBuilder').modal();
	},
	submit: function() {
		postData = {
			topic: questionBuilderModal.topic,
			title: $('#qbName').val(),
			words: $('#qbWords').val()
		}
		$.ajax({
			type: 'POST',
			url: '/teacher/createQuestion/',
			data: postData,
			success: function(result) {
				$('#questionBuilder').modal('toggle');
				$('.modal-backdrop').hide();
			}
		})
	}
}

function openEditTopicModal() {
	
}