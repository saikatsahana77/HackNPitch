document.getElementById("username").innerHTML = sessionStorage.getItem("email");


var k = "../profile/"+sessionStorage.getItem("email");
document.getElementById("profile_btn").setAttribute("href",k);


k = "../upload/"+sessionStorage.getItem("email");
document.getElementById("sell_btn").setAttribute("href",k);

k = "../products/"+sessionStorage.getItem("email");
document.getElementById("product_btn").setAttribute("href",k);


// var items = document.querySelectorAll(".items");
// var search = document.getElementById("search_btn");
// var query = document.getElementById("search");
// var tags = document.querySelectorAll(".tags");


// search.addEventListener("click", function() {
//     console.log("running");
//     console.log(tags);
//     tags.forEach((idx) => {
//         var string = idx.innerHTML;
//         var substring = query.value;
//         if (string.indexOf(substring) !== -1){
//             console.log(idx.parentElement);
//             var el = idx.parentElement;
//             // while(el.className != 'items'){
//             //     el = el.parentElement;
//             // }
//             el.style.display = "block";
//         }
//         else{
//             console.log(this);
//             var el = idx.parentElement;
//             // while(el.className != 'items'){
//             //     el = el.parentElement;
//             // }
//             el.style.display = "none";
//         }
//     })
// });


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