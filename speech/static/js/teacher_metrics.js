$(document).ready(function() {
    $('.ui.accordion').accordion();
    getStudentPerformance();
})

function getStudentPerformance() {
    $.ajax({
		type: 'GET',
		url: "/metrics/ajax/getStudentPerformance/",
		success: function (result) {
			console.log(result)
		}
	})
}