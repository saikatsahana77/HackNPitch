document.getElementById("username").innerHTML = sessionStorage.getItem("email");

var k = "../profile/"+sessionStorage.getItem("email");
document.getElementById("profile_btn").setAttribute("href",k);

var k = "../products/"+sessionStorage.getItem("email");
document.getElementById("product_btn").setAttribute("href",k);

k = "../cart/"+sessionStorage.getItem("email");
document.getElementById("cart_btn").setAttribute("href",k);

k = "../purchases/"+sessionStorage.getItem("email");
document.getElementById("purchase_btn").setAttribute("href",k);

k = "../dashboard/"+sessionStorage.getItem("email");
document.getElementById("dashboard_btn").setAttribute("href",k);

k = "../dashboard/"+sessionStorage.getItem("email");
document.getElementById("home_btn").setAttribute("href",k);


function add_sub() {
    var subject = document.getElementById("sub_book");
    var tags = document.getElementById("tags_book");
    if (tags.value==""){
        tags.value = subject.value;
    }
    else{
        tags.value = tags.value + ", " + subject.value;
    } 
}

function add_stream() {
    var stream = document.getElementById("stream_book");
    var tags = document.getElementById("tags_book");
    if (tags.value==""){
        tags.value = stream.value;
    }
    else{
        tags.value = tags.value + ", " + stream.value;
    } 
}