$(document).ready(function() {
$(".btn-how").on("click", function(){
	$('#myModal').modal('show');

});
$(".btn-fck").on("click", function(){
	$('#myModal').modal('hide');
	var url = $('#youtube-video').attr('src');

	//Then assign the src to null, this then stops the video been playing
	$('#youtube-video').attr('src', '');
	//
	//// Finally you reasign the URL back to your iframe, so when you hide and load it again you still have the link
	$('#youtube-video').attr('src', url);
});
	
	/*
	"use strict";
// --------------Newsletter-----------------------

	$(".newsletter-signup").ajaxChimp({
		callback: mailchimpResponse,
		url: "http://sandlabs.us9.list-manage.com/subscribe/post?u=a6801279da611bc55645c0413&id=9977eec545" // Replace your mailchimp post url inside double quote "".  
	});

	function mailchimpResponse(resp) {
		 if(resp.result === 'success') {
		 
			$('.alert-success').html(resp.msg).fadeIn().delay(3000).fadeOut();
			
		} else if(resp.result === 'error') {
			$('.alert-warning').html(resp.msg).fadeIn().delay(3000).fadeOut();
		}  
	};
*/
 });
