//AJAX POST request for review posting  
	var theForm = document.getElementById( 'theForm' );
	new stepsForm( theForm, {
		  onSubmit : function( form ) {
			// hide form
		  classie.addClass( theForm.querySelector( '.simform-inner' ), 'hide' );
	      var messageEl = theForm.querySelector( '.final-message' );
	      var rating  = $('#review_rating').val() 
	      var review_text  = $('#review_text').val() 

	        $.ajax({

	                url : "/add_rating/",
	                data : {'c_id':c_id,'rating':rating,'review_text':review_text,'csrfmiddlewaretoken': csrfmiddlewaretoken},
	                type : "POST",
	                success : function(json_from_view) {
	                	if(json_from_view){
				               messageEl.innerHTML = 'Thank You For Your Valuable Feedback';
	                     $('#u_review').text(review_text);
	                     $('#u_star').text('You rated '+rating+' stars.');
	                     current_width = $('#rating_bar_'+rating).width();
	                     if (current_width == 0){
	                       $('#rating_bar_'+rating).width(current_width+10)
	                     }
	                     else{
	                      if(current_width <= 97){
	                        $('#rating_bar_'+rating).width(current_width+3)
	                      }
	                     }
	                    }
	          				else{
	              			messageEl.innerHTML = 'We cannot save the review posted!!!';
	              			classie.addClass( messageEl, 'show' );
	                  }
	               },
	                // handle a non-successful response
	                error : function(xhr,errmsg,err) {
						messageEl.innerHTML = 'Error in posting the review! Try again.';
						classie.addClass( messageEl, 'show' );
	                 }
	            });
				
			}
	});
//AJAX GET request for review removal
function remove_review(){
	// confirm dialog
		alertify.confirm("You want to remove your rating ?", function (e) {
		    if (e) {
		        // user clicked "ok"
		        $.ajax({
		          url : "/remove_rating/",
		          data : {'c_id':c_id,'csrfmiddlewaretoken': csrfmiddlewaretoken},
		          type : "POST",

		          success : function(json_from_view) {
		          		if(json_from_view)
		          		   window.location = window.location;
		          		else
		          			 alertify.alert("Can't remove the review");
		         },
		          error : function(xhr,errmsg,err) {
		            console.log('error in removing review');
		      }
		      });
		    } else {
		    	alertify.error( 'Operation Cancelled' );
		        // user clicked "cancel"
		    }
		});
}