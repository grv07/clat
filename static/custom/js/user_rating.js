$('#rating_stars').click(function(event) {
	var rated = parseInt($(event.target).data('rate'));
	console.log(typeof(rated));
	if(isNaN(rated)){
		$('#ratedmsg').html('Click properly on the stars.');
		$('#post_review_button').prop('disabled',true);
		return false;
	}else{
		$('#post_review_button').prop('disabled',false);
	}
	if($("#rating_stars").find('[data-rate="'+rated+'"]').hasClass('glyphicon-star-empty')){
	for(i=rated;i>0;i--){
		var star = $("#rating_stars").find('[data-rate="'+i+'"]');
		if(star.hasClass('glyphicon-star-empty')){
			star.removeClass('glyphicon-star-empty')
			star.addClass('glyphicon-star');
		}
	}
}
	if($("#rating_stars").find('[data-rate="'+rated+'"]').hasClass('glyphicon-star')){
	for(i=rated+1;i<=5;i++){
	var star = $("#rating_stars").find('[data-rate="'+i+'"]');
	if(star.hasClass('glyphicon-star')){
			star.removeClass('glyphicon-star');
			star.addClass('glyphicon-star-empty');
		}
	}
}
	$('#ratedmsg').html('( You rated '+rated+' stars. )');
	$('#rated').val(rated);
});

//AJAX POST request for posting review
	function post_review(el,form) {
		// var rating  = $('#review_rating').val() 
	    var rated  = form.elements['rated'].value;
	    var review_text  = form.elements['review_text'].value;
	    if(review_text && rated){
		$.ajax({
		        url : "/add_rating/",
		        data : {'c_id':$(el).data('course'),'rating':rated,'review_text':review_text,'csrfmiddlewaretoken': $('#ctkn').val()},
		        type : "POST",
		        success : function(json_from_view) {
		        		window.location = window.location;
		       },
		        error : function(xhr,errmsg,err) {
					alert('Server error in posting the review! Try again.');
		         }
		    });
	}else{
		alert('Please rate and write a review.');
	}
	}	      

  //AJAX POST request for review removal
function remove_review(el){
  // confirm dialog
    // alertify.confirm("You want to remove your rating ?", function (e) {
    //     if (e) {
    //         $.ajax({
    //           url : "/remove_rating/",
    //           data : {'c_id':$(el).data('course'),'rating':$(el).data('rating'),'csrfmiddlewaretoken': $('#ctkn').val()},
    //           type : "POST",

    //           success : function(json_from_view) {
    //                 window.location = window.location;
    //             },
    //           error : function(xhr,errmsg,err) {
    //             alert('Server error in removing review.');
    //       }
    //       });
    //     } else {
    //      alertify.error('Operation Cancelled.');
    //     }
    // })};
	showConfirmModal("formSubmission", "You want to remove your rating ?", "#remove_review_form", "Review deletion cancelled.");
}