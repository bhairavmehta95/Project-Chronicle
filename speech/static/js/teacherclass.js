$(document).ready(function() {
	populateTopics();
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
		var link = $("<a onclick='questionBuilderModal.open(this)' class='question-link'></a>")
			.text(topicArray[i].fields.topic_name)
			.attr("topicNumber", topicArray[i].pk);
		var listElement = $("<li></li>");
		listElement.append(link);
		$('#topicList').append(listElement);
	}
}

function test(thing) {
	alert($(thing).text());
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