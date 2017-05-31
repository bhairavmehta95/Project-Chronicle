$(document).ready(function() {
	populateClasses();
})

function populateClasses() {
	$.ajax({
		type: 'GET',
		url: "/teacher/getClasses/",
		success: function (results) {
			console.log(results.length)
			results.forEach(function (myClass) {
				var data = myClass.fields;
				renderClass(data.class_name, data.num_enrollments);
			})
		}
	})
}

function renderClass(name, numEnrollments) {
	var newCard = $('#classContainer .card.template').clone();
	newCard.find('.header').text(name);
	newCard.find('.enrollments-count').text(numEnrollments);
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
		url: 'createClass/',
		data: postData,
		success: function(result) {
			renderClass(name, 0);
		}
	})
}