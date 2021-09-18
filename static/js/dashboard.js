document.getElementById("username").innerHTML = sessionStorage.getItem("email");


var k = "profile/"+sessionStorage.getItem("email");
document.getElementById("profile_btn").setAttribute("href",k);