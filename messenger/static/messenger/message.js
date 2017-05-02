$("#send").click(function(){
	var message = document.getElementbyId("message").value;
	$("#user").innerHTML = message;
});