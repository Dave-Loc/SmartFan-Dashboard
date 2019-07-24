//On page load
$(document).ready(function() {
	setInterval(function() 
		{
			$.ajax({
				type: "POST",
				url: "/"
			});
		}, 30000);
});
