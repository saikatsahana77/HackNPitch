document.getElementById("username").innerHTML = sessionStorage.getItem("email");


var k = "../profile/"+sessionStorage.getItem("email");
document.getElementById("profile_btn").setAttribute("href",k);


k = "../upload/"+sessionStorage.getItem("email");
document.getElementById("sell_btn").setAttribute("href",k);

k = "../products/"+sessionStorage.getItem("email");
document.getElementById("product_btn").setAttribute("href",k);

k = "../cart/"+sessionStorage.getItem("email");
document.getElementById("cart_btn").setAttribute("href",k);


function filter() {
    var filter = document.getElementById("search_box").value.toUpperCase();
    var items = document.querySelectorAll(".items");
    // var tags = items.getElementsByClassName("tags");

    for (var i= 0; i < items.length; i++){
        var tag = items[i].querySelectorAll(".tags")[0];
        if (tag){
            let value = tag.textContent || tag.innerHTML;
            if (value.toUpperCase().indexOf(filter) > -1){
                items[i].style.display = "";
            }else{
                items[i].style.display = "none";
            }
        }
    }
}


var j = document.getElementsByClassName("email_send_cont");
for (var i= 0; i < j.length; i++){
    j[i].value  = sessionStorage.getItem("email");
}
