$(document).ready(function() {
    $('.ui.accordion').accordion();
    getStudentPerformance();
    getQuestionStatistics();
})

function getStudentPerformance() {
    $.ajax({
		type: 'GET',
		url: "/metrics/ajax/getStudentPerformance/",
		success: function (results) {
			for (var key in results) {
				renderPerformance(results[key]);
            }
            $('#perfRowTemplate').remove();
		}
	})
}

function renderPerformance(data) {
    var $performances = $('#performances');
    var $row = $('#perfRowTemplate').clone();
    $row.data(data);
    $row.find('.class').text(data.class_name);
    $row.find('.name').text(data.student_name);
    $row.find('.total-responses').text(data.total_responses);
    $row.find('.total-questions').text(data.questions_attempted);
    $row.find('.total-passes').text(data.questions_passed);
    $row.removeAttr('id').removeClass('template').appendTo($performances);
}

function getQuestionStatistics() {
    $.ajax({
		type: 'GET',
		url: "/metrics/ajax/getQuestionStatistics/",
		success: function (results) {
			for (var key in results) {
				renderQuestionStats(results[key]);
            }
            $('#questionRowTemplate').remove();
		}
	})
}

function renderQuestionStats(data) {
    console.log(data)
    var $questions = $('#questions');
    var $row = $('#questionRowTemplate').clone();
    $row.data(data);
    $row.find('.question').text(data.question_name);
    $row.find('.responses').text(data.num_responses);
    $row.find('.passing').text(data.num_passed);
    $row.find('.average').text(data.average_score);
    $row.removeAttr('id').removeClass('template').appendTo($questions);
}