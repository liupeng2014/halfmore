$(function(){
	document.title = "HalfMore";
});

function search() {
	$("#search").attr("action", "/search");
	$("#search").submit();
}

function login() {
	$("#login").attr("action", "/login");
	$("#login").submit();
}