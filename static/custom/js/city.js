  $("#state").change(function(event) {
            $.ajax({
                    url : "/load_cities/",
                    data : { 'state' : $(this).val()},
                    type : "GET",

                    success : function(json_from_view) {
                                    $('#city').html('');

                for(var i=0;i<json_from_view.length;i++){
                $('#city').append('<option value="'+json_from_view[i]+'">'+json_from_view[i]+'</option>');
                }
                    },
                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {
                        $('#results').html("Cities are not loading!!!"); 
                            //console.log(xhr.status + ": " + xhr.responseText);         }
                }
                });
            });