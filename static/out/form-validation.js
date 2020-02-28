// Disable form submissions if there are invalid fields
(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Get the forms we want to add validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();
// Code example from w3schools.com
(function () {
    var myInput = document.getElementById('password');
    var letter = document.getElementById('letter');
    var capital = document.getElementById('capital');
    var number = document.getElementById('number');
    var length = document.getElementById('length');
    // When the user starts to type something inside the password field
    myInput.onkeyup = function () {
        // Validate lowercase letters
        var lowerCaseLetters = /[a-z]/g;
        if (myInput.value.match(lowerCaseLetters)) {
            letter.classList.remove('invalid');
            letter.classList.add('valid');
        }
        else {
            letter.classList.remove('valid');
            letter.classList.add('invalid');
        }
        // Validate capital letters
        var upperCaseLetters = /[A-Z]/g;
        if (myInput.value.match(upperCaseLetters)) {
            capital.classList.remove('invalid');
            capital.classList.add('valid');
        }
        else {
            capital.classList.remove('valid');
            capital.classList.add('invalid');
        }
        // Validate numbers
        var numbers = /[0-9]/g;
        if (myInput.value.match(numbers)) {
            number.classList.remove('invalid');
            number.classList.add('valid');
        }
        else {
            number.classList.remove('valid');
            number.classList.add('invalid');
        }
        // Validate length
        if (myInput.value.length >= 8) {
            length.classList.remove('invalid');
            length.classList.add('valid');
        }
        else {
            length.classList.remove('valid');
            length.classList.add('invalid');
        }
    };
})();
// /* Verify Registration Info */
// $(document).ready(function(){
//   $("#register").on("submit", function(e){
//     e.preventDefault();
//     $.getJSON("/check", {username: $("#username").val()}, function(data){
//         if (data == false){
//           document.getElementById("username-alert").style.display = "inline-block";
//           document.getElementById("register").reset();
//           letter.classList.remove("valid");
//           letter.classList.add("invalid");
//           capital.classList.remove("valid");
//           capital.classList.add("invalid");
//           number.classList.remove("valid");
//           number.classList.add("invalid");
//           length.classList.remove("valid");
//           length.classList.add("invalid");
//           $("#username").focus();
//         }
//         else
//         {
//           document.getElementById("register").submit();
//         }
//     });
//   });
// /* Verify Log In Credentials */
// $(document).ready(function(){
//   $("#user-login").submit(function(e) {
//       var form: any = this;
//       e.preventDefault();
//       var username = $("#username").val();
//       var password = $("#password").val();
//       $.post('/login',
//       {
//         username: username,
//         password: password
//       },
//       function(data) {
//         // Show alert or if user has wrong credentials
//         if(data === true) {
//           // $("#error_notif").show();
//           document.getElementById("login-alert").style.display = "inline-block";
//         } else {
//           // Return Flask jsonify if authentication was successfull
//               form.submit();
//         }
//     });
//   });
// });
//# sourceMappingURL=form-validation.js.map