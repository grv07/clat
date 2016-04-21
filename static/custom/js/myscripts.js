$(document).ready(function($) {

	$(document).tooltip({
	  position: {
	    my: "center bottom",
	    at: "center top",
	  }
	});

	$(document).tooltip({
		open: function(event, ui) {
	   	$(ui.tooltip).fadeTo(6000,0);
	    }
	})

	$('#myCarousel').carousel({
	  interval: 2000,
	  cycle: true
	});
});