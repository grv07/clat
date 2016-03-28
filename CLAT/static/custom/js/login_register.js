        $(function () {
            // get_city();
            // Setup form validation on the #register-form element
            $.validator.addMethod("pwcheck", function (value) {              
                return /^(?=.*?[a-zA-Z])(?=.*?[0-9])(?=.*?[@#&^%!*%$])[a-zA-Z0-9@#&^%!*%$]{8,20}$/.test(value) // consists of only these
                        && /[a-z]/.test(value)&& /[A-Z]/.test(value) // has a lowercase letter
                        && /\d/.test(value); // has a digit
            });
            $.validator.addMethod('checkUsername', function(username, element) {
                    var pattern = /^[a-zA-Z0-9_.-]+$/;
                    return pattern.test(username)
                    }, 'No spaces are allowed. Only _ . - special characters are allowed.');

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
            
            $('#reg_form').validate({
                // Specify the validation rules
                rules: {
                    username: {
                        required: true,
                        minlength: 4,
                        maxlength: 15,
                        checkUsername: true,
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
                        maxlength: 50
                    },  
                    password: {
                        required: true,
                        minlength: 8,
                        pwcheck: true,
                        maxlength: 20
                    },
                    password_confirm: {
                        required: true,
                        minlength: 8,
                        maxlength: 20,
                        equalTo: "#reg_password"
                    },
                    phone_number: {
                        required: true,
                        phoneUK:true,
                        remote: '/verify_phone_number/'
                    },
                    d_o_b:{
                        required:true,
                        date_val:true,
                    },
                    i_agree:"required",
                    street1:"required",
                    pincode: {
                        required: true,
                        pincodecheck: true,
                    },
                    higher_education:{
                        required: true,
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
                    username: {
                        required: "Please enter your username",
                        minlength: "Your username must be at least 4 characters long.",
                        maxlength: "Your username must be at most 15 characters long.",
                        remote: "This username was already used for signing up.",
                        checkUsername: "No spaces are allowed. Only _ . - special characters are allowed."
                    },
                    full_name: "Please enter your full name",
                    password: {
                        required: "Please provide a password",
                        minlength: 'Password must be at least 8 characters long, combination of capital, small letters, numbers and special characters, For example: @Tt12lo#',
                        pwcheck:'Password must be combination of capital, small letters, numbers and special characters, For example: @Tt12lo#',
                        maxlength: "Your password must be at most 20 characters long. For example: @Tt12lo#"
                    },
                    mailing_address: "Please enter a valid mailing address.",
                    password_confirm: {
                        required: "Please provide a confirm password.",
                        equalTo: "Password and confirm password must be same.",
                        minlength: "Your password must be at least 8 characters long.",
                        maxlength: "Your password must be at most 10 characters long."
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
                        date_val:'Please enter valid date'
                    },
                    country: 'Please enter valid country.',
                    city: 'Please enter valid city.',
                    state:'Please enter valid state.',
                    i_agree:'Please agree with eQuest Terms of Service first.',
                    street1:'Please enter street address.',
                    pincode: {
                        required: 'Please enter pincode.',
                        pincodecheck: 'Please enter valid pincode.',
                    },
                    higher_education:{
                        required: 'Please select higher education.',
                    }
                },

                submitHandler: function (form) {
                    form.submit();
                }
            });

        });
        
    //     $(function () {
    //     $("#login_form").validate(
    //             {
    //                 rules: {
    //                     username: {
    //                         required: true
    //                     },
    //                     password: {
    //                         required: true,
    //                     }
    //                 },
    //                 errorElement: 'p',
    //             highlight: function(element) {
    //                 $(element).parent().addClass("has-error");
    //                 $(element).addClass('error')
    //             },
    //             unhighlight: function(element) {
    //                 $(element).parent().removeClass("has-error");
    //                 $(element).removeClass('error')
    //             },
    //                 // messages: {
    //                 //     username: {
    //                 //         required: "Please enter your username"
    //                 //     },
    //                 //     password: {
    //                 //         required: "Please enter your password."
    //                 //     }
    //                 // }
    //             });

    // });
