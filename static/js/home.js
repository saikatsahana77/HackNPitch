function detect() {
    document.getElementById("password1").classList.add("pass_mismatch");
    document.getElementById("passHelp1").style.display = "block";
}

function passWeak() {
    document.getElementById("passHelp").style.display = "block";
}

var signup = document.getElementById("signup");

signup.addEventListener("submit", function(e) {
    var psd = document.getElementById("password").value;
    var conf_psd = document.getElementById("password1").value;
    var pass_regex=  newRegExp('((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,}))|((?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,}))');
    var errors= 0;
    if (psd !== conf_psd){
        errors+=1;
        detect()
    }
    if(psd.test(pass_regex) == false){
        errors+=1;
        passWeak();
    } 
    if (errors > 0)
    {
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

$(function() {
$('#otp').bind('click', function() {
    $.ajax('/send_otp', {
    type: 'POST', 
    data: {},
    success: function (data, status, xhr) {
    },
    error: function (jqXhr, textStatus, errorMessage) {
    }
});
    return false;
});
});

