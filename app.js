$('document').ready(function(){
	$('#hints').hide();
});

var count = 2;
$('#anonymous').click(function(){
	if(count % 2 === 0) {
		$('#hints').show();
	} else {
		$('#hints').hide();
	}
	count = count + 1;
});