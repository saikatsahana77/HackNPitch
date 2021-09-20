document.getElementById("username").innerHTML = sessionStorage.getItem("email");


var k = "../products/"+sessionStorage.getItem("email");
document.getElementById("product_btn").setAttribute("href",k);

k = "../dashboard/"+sessionStorage.getItem("email");
document.getElementById("dashboard_btn").setAttribute("href",k);

k = "../dashboard/"+sessionStorage.getItem("email");
document.getElementById("dashboard_btn").setAttribute("href",k);