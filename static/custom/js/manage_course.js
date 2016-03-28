    $(document).ready(function(){

      $('#course_type > option[value="{{course.course_sectors_and_associates}}"]').prop('selected', true);


      for(var i=1;i<=parseInt('{{weeks}}');i++){
                $('#week').append('<option value="'+i+'">'+'Week '+i+'</option>');
                }
      $('select').material_select();    
      $('.caret').remove();

    getModules();
        });


    function getModules(){
      $.ajax({
                    url : "/load_modules/",
                    data : { 'week' : $('#week').val(),'_c_id' : '{{course.course_uuid}}'},
                    type : "GET",

                    success : function(json_from_view) {
                      $('#module').empty().html('');
                       $('#results').empty().html('');
                       if(json_from_view.length!=0){
                for(var i=0;i<json_from_view.length;i++){
                $('#module').append('<option value="'+json_from_view[i]+'">'+json_from_view[i]+'</option>');
                }
              }
              else{
              $('#results').html("No modules present!!!"); 
              $('#module').append('<option value="">Nothing</option>');
              $('#update_details_button').prop('disabled',true);


              }
              $('#module').material_select();
                 $('.caret').remove();
                },
                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {
                      $('#update_details_button').prop('disabled',true);
                        $('#results').html("Modules are not loading!!!"); 
                            //console.log(xhr.status + ": " + xhr.responseText);         }
                }
                });
    }


function getWeekDetails(){
      $.ajax({
                    url : "/load_week_details/",
                    data : { 'week' : $('#week').val(),'_c_id' : '{{course.course_uuid}}','module' : $('#module').val() },
                    type : "GET",

                    success : function(json_from_view) {
                      $('#update_details_button').prop('disabled',false);
                      $('#delete_module_button').prop('disabled',false);

                      if(json_from_view.length!=0){
                      $('#week_details').html('');
                      $('#results_week_detail').html('');
                      $('#week_details').html(json_from_view);
                    }else{
                        $('#results_week_detail').html("Week Details are not loading!!!"); 
                        $('#update_details_button').prop('disabled',true);
                        $('#delete_module_button').prop('disabled',true);

                    }
                    }
                ,
                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {
                      $('#update_details_button').prop('disabled',true);
                      $('#delete_module_button').prop('disabled',true);
                      $('#results_week_detail').html("Week Detail are not loading!!!"); 
                            //console.log(xhr.status + ": " + xhr.responseText);         }
                }
                });
    }


  //AJAX GET request for loading modules when a week is selected or changed
  $("#week").change(function(event) {
            getModules();
        });



  $('#module').change(function(event) {
    // $('#new_module_name').html($(event.target).val());
                getWeekDetails();

  });



  $('#update_details_button').click(function(event) {
  	$.ajax({
                    url : "/teacher/update/course/week/details/",

                    data : { '_week' : $('#week').val(),'_c_id' : '{{course.course_uuid}}','_module' : $('#module').val(),'_week_details':$('#week_details').val(),'csrfmiddlewaretoken': '{{ csrf_token }}' },
                    type : "POST",

                    success : function(json_from_view) {
                                            $('#update_details_button').prop('disabled',false);

                      if(json_from_view){
                      window.location = window.location;
                    }else{
                        alert('Cannot save your details!!!'); 
                        $('#update_details_button').prop('disabled',true);

                    }
                    },
                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {
                      $('#update_details_button').prop('disabled',true);

                        alert('Error in updating the details!!!'); 
                            //console.log(xhr.status + ": " + xhr.responseText);         }
                }
                });
  });



$('#update_course_details_button').click(function(event) {
  $.ajax({
                    url : "/teacher/update/course/details/",
                    data : { '_c_desc':$('#course_description').val(), '_c_objve':$('#course_objective').val(), '_c_id' : '{{course.course_uuid}}','csrfmiddlewaretoken': '{{ csrf_token }}' },
                    type : "POST",

                    success : function(json_from_view) {
                      if(json_from_view){
                      window.location = window.location;
                    }else{
                        alert('Cannot update the course details!!!'); 

                    }
                    },
                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {

                        alert('Error in updating the details!!!'); 
                            //console.log(xhr.status + ": " + xhr.responseText);         }
                }
                });
              
      });





  $('#course_image_file_upload').change(function(event) {
      var extension_of_picture = $(this).val().split('.').pop().toLowerCase();

    if(['jpeg','jpg','gif','png', 'JPEG', 'JPG', 'GIF', 'PNG'].indexOf(extension_of_picture) === -1 )
    {      
      alert('Only jpg,gif and png files are allowed!!!');
    }

  });



  $('#course_type_name_update_details_button').click(function(event) {
      $.ajax({
                      url : "/teacher/update/course/typeandname/",

                      data : { '_c_name' : $('#course_name').val(), '_c_type' : $('#course_type').val() ,'_c_id' : '{{course.course_uuid}}','csrfmiddlewaretoken': '{{ csrf_token }}' },
                      type : "POST",

                      success : function(json_from_view) {

                        if(json_from_view){
                        window.location.reload();
                      }else{
                          alert('Cannot save new course and type!!!'); 
                      }
                      },
                      // handle a non-successful response
                      error : function(xhr,errmsg,err) {
                          alert('Error in updating the course name and type!!!'); 
                              //console.log(xhr.status + ": " + xhr.responseText);         }
                  }
                  });
    });




  $('#delete_module_button').click(function(event) {
    $.ajax({
                      url : "/teacher/delete/module/",
                      data : { '_week' : $('#week').val(),'_c_id' : '{{course.course_uuid}}','_module' : $('#module').val(),'csrfmiddlewaretoken': '{{ csrf_token }}' },
                      type : "POST",

                      success : function(json_from_view) {
                        if(json_from_view){
                        window.location = window.location;
                      }else{
                          alert('Cannot delete the course module '+$('#module').val()+' under week '+ $('#week').val()); 

                      }
                      },
                      // handle a non-successful response
                      error : function(xhr,errmsg,err) {

                          alert('Error in deleting the module!!!'); 
                              //console.log(xhr.status + ": " + xhr.responseText);         }
                  }
                  });
                
        });
