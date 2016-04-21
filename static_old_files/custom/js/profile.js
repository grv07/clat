$(function () {
            // get_city();
            // Setup form validation on the #register-form elemen

            $.validator.addMethod('phoneUK', function(phone_number, element) {
                    var pattern = /^([789]\d{9})$/;
                    return pattern.test(phone_number)
                    }, 'Phone number must be in Indian format.');

            $.validator.addMethod('pincodecheck', function(pincode, element) {
                    var pattern = /^(\d{6})$/;
                    return pattern.test(pincode)
                    }, 'Please specify a valid pincode.');

            $.validator.addMethod('date_val', function(d_o_b, element) {
                    var pattern = /^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d+$/;
                    return pattern.test(d_o_b)
                    }, 'Please enter a valid date.');

            $.validator.addMethod('fblinkcheck', function(fblink, element) {
                    if(fblink.indexOf('facebook') != -1)
                        return true;
                    return false;
                    }, 'Please enter a facebook profile link.');

            $.validator.addMethod('glinkcheck', function(glink, element) {
                    if(glink.indexOf('google') != -1)
                        return true;
                    return false;
                    }, 'Please enter a google profile link.');
            
            $('#update_profile_details_form').validate({
                // Specify the validation rules
                rules: {
                    username: {
                        required: true,
                        remote: '/verify_username/'
                    },
                    full_name: "required",
                    country: "required",
                    city: "required",
                    state: "required",
                    email: {
                        required: true,
                        email: true,
                        remote: '/verify_email/',
                    },  
                    
                    phone_number: {
                        required: true,
                        phoneUK:true,
                        remote: '/verify_phone_number/',
                    },
                    d_o_b:{
                        required:true,
                        date_val:true,
                    },
                    i_agree:"required",
                    street1:"required",
                    pincode: {
                        required: true,
                        pincodecheck: true
                    },
                    higher_education: {
                        required: true,
                    },
                    // fblink:{
                    //     required: false,
                    //     fblinkcheck: true
                    // },
                    // glink:{
                    //     required: false,
                    //     glinkcheck: true
                    // }
                },
                errorElement: 'p',
                highlight: function(element) {
                    $(element).parent().addClass("has-error");
                    $(element).addClass('error')
                },
                unhighlight: function(element) {
                    $(element).parent().removeClass("has-error");
                    $(element).removeClass('error')
                },


                // Specify the validation error messages
                messages: {
                    username: {
                        required: "Please enter your username",
                        remote: "This username was already used for signing up.",
                    },
                    full_name: "Please enter your full name",
                    password: {
                        required: "Please provide a password",
                        minlength: 'Password must be at least 8 characters long, combination of capital, small letters, numbers and special characters, For example: @Tt12lo#',
                        pwcheck:'Password must be combination of capital, small letters, numbers and special characters, For example: @Tt12lo#',
                        maxlength: "Your password must be at most 20 characters long. For example: @Tt12lo#"
                    },
                    email: {
                        required: "Please enter a valid email address.",
                        remote: "This email was already used for signing up."
                    },
                    phone_number : {
                        required :  "Please enter phone number.",
                        phoneUK  : "Phone number must be in Indian format.", 
                        remote : "We have a user with this phone number",
                    },
                    d_o_b:{
                        required:"Please enter Date of Birth",
                    },
                    country: 'Please enter valid country.',
                    city: 'Please enter valid city.',
                    state:'Please enter valid state.',
                    i_agree:'Please agree with Clat Terms of Service first.',
                    street1:'Please enter street address.',
                    pincode: {
                        required: 'Please enter pincode.',
                        pincodecheck: 'Please enter valid pincode.',
                    },
                    higher_education: {
                        required: 'Please enter higher education.',
                    },
                    // fblink:{
                    //     fblinkcheck: 'Must be a facebook profile link.'
                    // },
                    // glink:{
                    //     glinkcheck: 'Must be a google profile link.'
                    // }
                },

                submitHandler: function (form) {
                    form.submit();
                }
            });

        });

function get_recent_image(){
        $('#profile_picture').attr('src','../../../static/images/profile_loader.gif');
         $.ajax({
            type:'GET',
            url: '/profile/picture/',
            // data:formData,
            cache:false,
            contentType: false,
            processData: false,
            success:function(data){
                console.log("success");
                // console.log(data);
                // console.log(data['status']);
                pic_src_url = data['file_name'];

                $('#profile_picture').attr('src',pic_src_url);
            },
            error: function(data){
                console.log("error");
                console.log(data);
                pic_src_url = data['file_name'];
                console.log(pic_src_url);
                $('#profile_picture').attr('src',pic_src_url);
            }
        });
}
$('#update_profile_picture_form').on('submit',(function(e) {
    $('#profile_picture').attr('src','../../../static/images/profile_loader.gif');
        e.preventDefault();
        var formData = new FormData(this);
        // alert('call')
        $.ajax({
            type:'POST',
            url: $(this).attr('action'),
            data:formData,
            cache:false,
            contentType: false,
            processData: false,
            success:function(data){
                console.log("success");
                // console.log(data);
                // console.log(data['status']);
                pic_src_url = data['file_name'];

                $('#profile_picture').attr('src',pic_src_url);
                // alert('reload...')
                window.location=window.location;
            },
            error: function(data){
                console.log("error");
                console.log(data);
            },
            xhrFields: {
      // add listener to XMLHTTPRequest object directly for progress (jquery doesn't have this yet)
      onprogress: function (progress) {
        // calculate upload progress
        // var percentage = Math.floor((progress.total / progress.totalSize) * 100);
        // log upload progress to console
        // alert(progress.loaded);
        // alert(findSize());
        // console.log('progress', percentage);
        // if (percentage === 100) {
          console.log('DONE!');
        // }
      }
    }
        });
    }));

//AJAX GET request for loading cities when a state in selected or changed
window.onload=getCities;
function getCities(){
    console.log('getcities');
            $.ajax({
                    url : "/load_cities/",
                    data : { 'state' : $("#state").val()},
                    type : "GET",
                    success : function(json_from_view) {
                      $('#city').empty().html('');
                       $('#results').empty().html('');
                        for(var i=0;i<json_from_view.length;i++){
                        $('#city').append('<option value="'+json_from_view[i]+'">'+json_from_view[i]+'</option>');
                        } 
                        setCity();
                    },
                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {
                        $('#results').html("Cities are not loading!!!"); 
                            //console.log(xhr.status + ": " + xhr.responseText);         }
                }
                });
            }
//AJAX GET request for loading cities when a state in selected or changed
$("#state").change(function(event) {
            $.ajax({
                    url : "/load_cities/",
                    data : { 'state' : $(this).val()},
                    type : "GET",
                    success : function(json_from_view) {
                      $('#city').empty().html('');
                       $('#results').empty().html('');
                          for(var i=0;i<json_from_view.length;i++){
                          $('#city').append('<option value="'+json_from_view[i]+'">'+json_from_view[i]+'</option>');
                          }

                             },
                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {
                        $('#results').html("Cities are not loading!!!"); 
                }
                });
            });

  $(document).ready(function() {

    // Datepicker Popups calender to Choose date.
    $(function() {
    $("#d_o_b").datepicker({
            changeMonth: true,
            changeYear: true,
            yearRange: "-50:+0",
            // minDate: "+20Y",
            maxDate: "-15Y"
    });
    });

    var first_pic_src_url = $('#profile_picture').attr('src');

    $('#upload_picture_button').click(function(event) {
      $('#uploaded_picture').click();
    });

  $('#uploaded_picture').change(function(event) {
      var extension_of_picture = $(this).val().split('.').pop().toLowerCase();

    if(['jpeg','jpg','gif','png', 'JPEG', 'JPG', 'GIF', 'PNG'].indexOf(extension_of_picture) != -1 )
    {
      $('#update_details_button').prop('disabled',false);      
      if($(this).val()){
          // $('#picture_alert').html('<p style="color:blue;">You selected : </p>'+$(this).val().replace(/.*[\/\\]/, ''));
          $('#clear_uploaded_picture').css('display','inline-block');
          $("#update_profile_picture_form").submit();
        }
      else
          $('#picture_alert').html('You selected nothing!!!');
    }
    else{
      $('#update_details_button').prop('disabled',true);
      alert('Only jpg,gif and png files are allowed!!!');
    }

  });
  
  $('#remove_picture_button').click(function(event) {
    $('#profile_picture').attr('src','../../../static/images/profile_loader.gif');
    $.ajax({
            url : "/remove_profile_picture/",
            data : { 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            type : "POST",
            success : function(json_from_view) {
              if(json_from_view){
                $('#picture_alert').css('color','blue');
                $('#picture_alert').html('Profile picture removed.');
                first_pic_src_url = '/CLAT_videos/media/profile_images/CLAT_default_DP.png';
                $('#profile_picture').attr('src',first_pic_src_url);
              }

              else{
                $('#picture_alert').html('Cannot remove the default profile picture.');
                $('#picture_alert').css('color','red');
              }
                $('#remove_picture_button').prop('disabled',true);
                window.location=window.location;
           },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#picture_alert').html("Error in request for removing the profile picture!!!"); 
                $('#picture_alert').css('color','red');         

        }
        });
  });
  });

  $('#reset_picture_button').click(function(event) {
    var el = $('#uploaded_picture');
    el.wrap('<form>').closest('form').get(0).reset();
    el.unwrap();
    $('#picture_alert').html('Your selection has been reset!!!');
    });


  function validate_file(){
     if($("#uploaded_picture").val() === ''){
        $('#picture_alert').html('Select an image first (formats : png, gif,& jpg).');
        return false;
     }
    return true;
}

  
$('#update_details_button').click(function(event) {
    alertify.confirm("Do you really want to update the profile ?", function (e) {
    if (e) {
        $('#update_profile_details_form').submit();
    } else {
        alertify.error( 'Operation Cancelled' );
        // user clicked "cancel"
    }
}).autoOk(5);
});
