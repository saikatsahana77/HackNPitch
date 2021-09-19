document.getElementById("username").innerHTML = sessionStorage.getItem("email");

var k = "../profile/"+sessionStorage.getItem("email");
document.getElementById("profile_btn").setAttribute("href",k);


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