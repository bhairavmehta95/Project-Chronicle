function loginClick() {
	$('.item.register').removeClass('active');
	$('.item.login').addClass('active');
	$('#loginForm').show();
	$('#signupForm').hide();
}

function registerClick() {
	$('.item.register').addClass('active');
	$('.item.login').removeClass('active');
	$('#loginForm').hide();
	$('#signupForm').show();
}