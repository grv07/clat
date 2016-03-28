function addRatings(rating,course_key) {
                // Changing the previous deletion modal to be used for rating permission modal
                $("#modal_body_content").html('<h2>Do you want to rate '+rating+' star(s)???</h2>');
                $("#confirm").html('Rate It');
                $("#confirm_modal").modal('show');

                // If permission is granted then initiate an AJAX call
                $("#confirm").click(function(){
                    $("#confirm_modal").modal('hide');
                     $.getJSON('/add/ratings/' + course_key, {'rating': rating}, function (data) {
                    if(data[0]==1){
                        $('#rating_info').html('You rated '+data[1]);
                        $('#starRating').html(data[2])
                       }
                    else{
                     $('#rating_info').html(data[1]);
                      }
                });
                });
        
            }

// Make a ajax call for paginate
function paginate(page) {
                console.log(page) 
                $.getJSON('/temp/?page=' + page, {}, function (data) {
                    console.log(data);
                    $('#uniqe').html('')
                    $('#uniqe').html(data.html)
                });
            }