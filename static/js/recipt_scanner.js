
var reader = undefined;
var extension = undefined;

var accepted_files = ['jpg', 'jpeg', 'png'];

function previewFile() {
    var preview = document.getElementById("image_preview");
    // var preview_container = document.getElementById("preview_container");
    var file = document.querySelector('input[type=file]').files[0];
    extension = file.name.split('.').pop().toLowerCase()

    reader = new FileReader();

    reader.addEventListener("load", function () {
        preview.src = reader.result;
        // preview_container.style.display = "block";
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}


$(document).ready(function () {


});