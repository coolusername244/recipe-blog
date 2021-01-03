  let i = 3

$(document).ready(function(){
    $('.sidenav').sidenav({edge: "top"});
    $('select').formSelect();
});

document.getElementById("add_new").addEventListener("click", function() {
    i++;
    let html = `<div class="row step">
                    <div class="input-field col s12 m2 center">
                        <strong class="">Step ${i}:</strong>
                    </div>
                    <div class="col s10 offset-s1 m10">
                        <textarea id="step_${i}" name="step[]" minlength="5" class="materialize-textarea validate required"></textarea>
                    </div>
                </div>`
    $('.steps').append(html);
});
