        $(function () {
            // get_city();
            // Setup form validation on the #register-form element
            $.validator.addMethod("pwcheck", function (value) {
                        return /^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[@#&^%!*%$])[a-zA-Z0-9@#&^%!*%$]{8,20}$/.test(value) // consists of only these
                        && /[a-z]/.test(value)&& /[A-Z]/.test(value) // has a lowercase letter
                        && /\d/.test(value); // has a digit
            });
            $('#change_password_form').validate({
                // Specify the validation rules
                rules: { 
                    new_password: {
                        required: true,
                        minlength: 8,
                        maxlength: 20,
                        pwcheck: true
                        
                    },
                    confirm_password: {
                        required: true,
                        minlength: 8,
                        maxlength: 20,
                        equalTo: "#new_password"
                    },
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
                    new_password: {
                        minlength: 'Password must be at least 8 characters long, combination of capital, small letters, numbers and special characters, For example: @Tt12lo#',
                        pwcheck:'Password must be combination of capital, small letters, numbers and special characters, For example: @Tt12lo#',
                        maxlength: "Your password must be at most 20 characters long. For example: @Tt12lo#"
                    },
                    confirm_password: {
                        minlength: 'Password must be at least 8 characters long, combination of capital, small letters, numbers and special characters, For example: @Tt12lo#',
                        maxlength: "Your password must be at most 20 characters long. For example: @Tt12lo#",
                        equalTo : "Passwords do not match"
                    },
                },
                submitHandler: function (form) {
                    form.submit();
                }
            });

        });

