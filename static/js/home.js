// Todetect the password mismatch
function detect() {
    document.getElementById("password1_signup").classList.add("pass_mismatch");
    document.getElementById("passHelp1").style.display = "block";
}

// To detect the password match
function detect_1() {
    document.getElementById("password1_signup").classList.remove("pass_mismatch");
    document.getElementById("passHelp1").style.display = "none";
}

// To detect weak password
function passWeak() {
    document.getElementById("passHelp").style.display = "block";
}

// To detect strong password
function passWeak_1() {
    document.getElementById("passHelp").style.display = "none";
}

// To detect the wrong phone number
function phoneWrong() {
    document.getElementById("phoneHelp").style.display = "block";
}

// To detect the correct phone number
function phoneWrong_1() {
    document.getElementById("phoneHelp").style.display = "none";
}

var otp ="";
var email = "";

// To check the value of email filled during password reset
function fill_email(){
    email = document.getElementById("email_otp_check").value;
}

var passw=  /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;//regex to check strong password
var signup = document.getElementById("signup");

// Handling the submission of creation of a new user
signup.addEventListener("submit", function (e) {
    if (document.getElementById("password_signup").value !== document.getElementById("password1_signup").value || document.getElementById("password_signup").value.match(passw) == null || document.getElementById("email_verify_otpHelp").innerHTML==="Incorrect OTP!" || document.getElementById("phone").value.length !== 10){
        e.preventDefault();
        if (document.getElementById("password_signup").value !== document.getElementById("password1_signup").value){
            detect();
        }
        else{
            detect_1();
        }
        if (document.getElementById("password_signup").value.match(passw) == null) {
            passWeak();
        }
        else{
            passWeak_1();
        }
        if (document.getElementById("phone").value.length !== 10) {
            phoneWrong();
        }
        else{
            phoneWrong_1();
        }
    } 
});


var login = document.getElementById("signIn");

// Handling the login of a user
login.addEventListener("submit", function(e){
    sessionStorage.setItem("email", document.getElementById("email_store").value);
    if (document.getElementById("email_store").value === ""){
        e.preventDefault();
    }
})

// Handling the signup success of an user
function signup_success(){
    swal("Signup Success", "Please login to proceed further!", "success");
}

// Handling the signup failure of an user
function signup_failure(){
    swal("Signup Failed", "User is already registered!", "error");
}

// Handling the slogin failure of an user
function login_failure(){
    swal("Login Failed", "Invalid email or password!", "error");
}

// To reset the password of an existing user
function pass_reset(){
    swal("Password Reset", "Your Password has been reset!", "success");
}

// AJAX call to send otp to new user to check his/her email(uses jQuery)
$(function() {
$('#otp').bind('click', function() {
    $.ajax('/send_otp', {
    type: 'POST', 
    data: {email: $('#email_otp_check').val()},
    success: function (data, status, xhr) {
        otp = data
    },
    error: function (jqXhr, textStatus, errorMessage) {
    }
});
    return false;
});
});

// AJAX call to send otp to a existing user(uses jQuery)
$(function() {
    $('#otp_verify').bind('click', function() {
        $.ajax('/send_otp_check', {
        type: 'POST', 
        data: {email: $('#email_check_otp').val()},
        success: function (data, status, xhr) {
            otp = data
        },
        error: function (jqXhr, textStatus, errorMessage) {
        }
    });
        return false;
    });
    });

// Fubction to check otp for password reset
function check_otp(){
    var confirm_otp = document.getElementById("box_otp").value;
    if (confirm_otp !== otp){
        document.getElementById("otpHelp").style.display = "block";
    }
    else{
        document.getElementById("otp_confirm").setAttribute("data-bs-toggle","modal");
        document.getElementById("otp_confirm").setAttribute("data-bs-target","#newPassModal");
        document.getElementById("otp_confirm").click();
        document.getElementById("email_final").value = email;
    }
}

// Fubction to check otp for email confirmation
function check_otp_1(){
    var confirm_otp = document.getElementById("box_email_verify_otp").value;
    if (confirm_otp !== otp){
        document.getElementById("email_verify_otpHelp").style.display = "block";
    }
    else{
        document.getElementById("email_verify_otpHelp").innerHTML = "Correct OTP!";
        document.getElementById("email_verify_otpHelp").style.color = "green";
        document.getElementById("email_verify_otpHelp").style.display = "block";
    }
}