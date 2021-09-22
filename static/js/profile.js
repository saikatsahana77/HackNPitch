// Setting the username
document.getElementById("username").innerHTML = sessionStorage.getItem("email");

// Setting the routes of the user properly
var k = "../products/"+sessionStorage.getItem("email");
document.getElementById("product_btn").setAttribute("href",k);

k = "../dashboard/"+sessionStorage.getItem("email");
document.getElementById("dashboard_btn").setAttribute("href",k);

k = "../purchases/"+sessionStorage.getItem("email");
document.getElementById("purchase_btn").setAttribute("href",k);

k = "../cart/"+sessionStorage.getItem("email");
document.getElementById("cart_btn").setAttribute("href",k);

k = "../dashboard/"+sessionStorage.getItem("email");
document.getElementById("home_btn").setAttribute("href",k);