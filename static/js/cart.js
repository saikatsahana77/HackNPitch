document.getElementById("username").innerHTML = sessionStorage.getItem("email");


var k = "../profile/"+sessionStorage.getItem("email");
document.getElementById("profile_btn").setAttribute("href",k);

k = "../products/"+sessionStorage.getItem("email");
document.getElementById("product_btn").setAttribute("href",k);

k = "../dashboard/"+sessionStorage.getItem("email");
document.getElementById("dashboard_btn").setAttribute("href",k);

k = "../purchases/"+sessionStorage.getItem("email");
document.getElementById("purchase_btn").setAttribute("href",k);

k = "../dashboard/"+sessionStorage.getItem("email");
document.getElementById("home_btn").setAttribute("href",k);

var j = document.getElementsByClassName("email_send_cont");
for (var i= 0; i < j.length; i++){
    j[i].value  = sessionStorage.getItem("email");
}


