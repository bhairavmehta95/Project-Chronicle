$(document).ready(function() {
	populateClasses();
})

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

function renderClass(data) {
	var newCard = $('#classContainer .card.template').clone();
	newCard.find('.header').text(data.class_name);
	newCard.find('.enrollments-count').text(data.num_enrollments);
	newCard.find('.class-key').text(data.class_key);
	newCard.data(data)
	newCard.removeClass('template').appendTo('#classContainer');
}

function openAddClassModal() {
	$('#newClassName').val('');
	$('#addClassModal')
	  .modal({
	    onApprove : function() {
	      submitModal('addClass');
	    }
	  })
	  .modal('show');
}

function submitModal(modalAction) {
	switch (modalAction) {
		case 'addClass':
			name = $('#newClassName').val();
			addClass(name);
			break;
	}
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
			data = $.parseJSON(result);
			console.log(result);
			console.log(result.fields);
			renderClass(data);
		}
	})
}