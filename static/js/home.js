function detect() {
    document.getElementById("password1_signup").classList.add("pass_mismatch");
    document.getElementById("passHelp1").style.display = "block";
}

function detect_1() {
    document.getElementById("password1_signup").classList.remove("pass_mismatch");
    document.getElementById("passHelp1").style.display = "none";
}

function passWeak() {
    document.getElementById("passHelp").style.display = "block";
}

function passWeak_1() {
    document.getElementById("passHelp").style.display = "none";
}

function phoneWrong() {
    document.getElementById("phoneHelp").style.display = "block";
}

function phoneWrong_1() {
    document.getElementById("phoneHelp").style.display = "none";
}

var otp ="";
var email = "";


function fill_email(){
    email = document.getElementById("email_otp_check").value;
}

var passw=  /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
var signup = document.getElementById("signup");

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

login.addEventListener("submit", function(e){
    // e.preventDefault();
    sessionStorage.setItem("email", document.getElementById("email_store").value);
    if (document.getElementById("email_store").value === ""){
        e.preventDefault();
    }
})


function signup_success(){
    swal("Signup Success", "Please login to proceed further!", "success");
}

function signup_failure(){
    swal("Signup Failed", "User is already registered!", "error");
}

function login_failure(){
    swal("Login Failed", "Invalid email or password!", "error");
}

function pass_reset(){
    swal("Password Reset", "Your Password has been reset!", "success");
}

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