
        $(function () {
            var reuse_course_name = {
                required: true,
                remote: '/verify-course-name/'
            };
            var reuse_course_name_msg = {
                required: "Please enter your course name",
                remote: "This course name was already used for course."
            };

            var reuse_course_duration = {
                required: true,
                number: true
            };
            var reuse_course_duration_msg = {
                required: "Please enter a valid course duration",
                number: "Course duration is must be in number"
            };
            var reuse_course_desc_msg = {
                required: "Please enter a valid course description",
                maxlength: "Course description must be under 1000 characters"
            };
            var reuse_course_objective_msg = {
                required: "Please enter a valid course objective",
                maxlength: "Course description must be under 600 characters"
            }

            $.validator.addMethod("file_name", function (value, element) {
                console.log(value.indexOf('.zip') >= 0);
                if (value.indexOf('.zip') >= 0 || value.indexOf('.mp4') >= 0) {
                    return true;
                }
                else {
                    return false;
                }
            }, 'File should be a zip file or a mp4 file');
            $.validator.addMethod("time24", function(value, element) {
                    return /^([01]?[0-9]|2[0-3])(:[0-5][0-9]){2}$/.test(value) || /^([0-9]|2[0-3])(:[0]?[0-5][0-9]){2}$/.test(value);
                }, "Invalid time format.");

            $.validator.addMethod("utb_file_name", function (value, element) {
                console.log(value.indexOf('youtube.com') >= 0);
                if (value.indexOf('www.youtube.com') >= 0 && value.indexOf('?v=') >= 0) {
                    return true;
                }
                else {
                    return false;
                }
            }, 'Please enter a video youtube URL ex:https://www.youtube.com/watch?v=yD-eQFyT1jM .');

            // Setup form validation on the #register-form element
            $("#articulate_file_form").validate({

                // Specify the validation rules
                rules: {
                    course_name: reuse_course_name,
                    articulate_file: {
                        required: true,
                        file_name: true
                    },
                    youtube_demo_url: {required: true},
                    // course_durations: reuse_course_duration,
                    course_start_date : {required:true,date:true},
                    course_end_date : {required:true,date:true},
                    course_start_time : {required:true/*,time24:true*/},
                    course_end_time : {required:true/*,time24:true*/},

                    course_description: {
                        required: true,
                        maxlength: 650
                    }
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
                    course_name: reuse_course_name_msg,
                    articulate_file: {
                        required: "Please upload a .mp4 file."
                    },
                    youtube_demo_url: {
                        required: "Please enter a video youtube URL eg. https://www.youtube.com/watch?v=yD-eQFyT1jM"
                    },
                    course_durations: reuse_course_duration_msg,
                    course_description: reuse_course_desc_msg,
                    course_start_date: 'Please add valid start date',
                    course_end_date: 'Please add valid end date',
                    course_start_time: 'Please add start time',
                    course_end_time: 'Please add end time',
                    course_objective: reuse_course_objective_msg,
                },

                submitHandler: function (form) {
                    form.submit();
                }
            });
            $("#utb_file_form").validate({

                // Specify the validation rules
                rules: {
                    course_name: reuse_course_name,
                    you_tube_url: {
                        required: true,
                        url: true,
                        utb_file_name: true
                    },
                    // course_durations: reuse_course_duration,
                    course_start_date : {required:true,date:true},
                    course_end_date : {required:true,date:true},
                    course_start_time : {required:true/*,time24:true*/},
                    course_end_time : {required:true/*,time24:true*/},

                    course_description: {
                        required: true,
                        maxlength: 1000
                    },
                    course_objective: {
                        required: true,
                        maxlength: 600
                    }
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
                    course_name: reuse_course_name_msg,
                    youtube_demo_url: {
                        required: "Please enter correct Youtube link."
                    },
                    // course_durations: reuse_course_duration_msg,
                    course_start_date: 'Please add valid start date',
                    course_end_date: 'Please add valid end date',
                    course_start_time: 'Please add valid start time',
                    course_end_time: 'Please add valid end time',
                    course_description: reuse_course_desc_msg,
                    course_objective: reuse_course_objective_msg

                },

                submitHandler: function (form) {
                    form.submit();
                }
            });

        });


    
        function change_form(button_id) {
            if (button_id == 'upload_you_file') {
                console.log('upload you tube button click !')
                $('#upload_you_file').prop('disabled', true);
                $('#upload_articulate_file').prop('disabled', false);
                $('#articulate_file_form').hide()
                $('#you_tube_form').show()
            }
            if (button_id == 'upload_articulate_file') {
                $('#upload_articulate_file').prop('disabled', true);
                $('#upload_you_file').prop('disabled', false);
                console.log('upload upload_articulate_file button click !')
                $('#you_tube_form').hide()
                $('#articulate_file_form').show()

            }
        }

        function updateVideo() {
            console.log($('#video_url').val());
            var new_youtube_url = $('#video_url').val();
            new_youtube_url_array = new_youtube_url.split('?v=');
            $('#iframe_place').html('');
            $('#iframe_place').html('<iframe id="video_iframe" width="560" height="315" src="http://www.youtube.com/v/' + new_youtube_url_array[1] + '"' +
                    'frameborder="0" allowfullscreen></iframe>');
        }


    