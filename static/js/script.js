  let i = 3

$(document).ready(function(){
    $('.sidenav').sidenav({edge: "top"});
    $('select').formSelect();
});

document.getElementById("add_new").addEventListener("click", function() {
    i++;
    let html = `<div class="row step">
                    <div class="input-field col s2 center">
                        <strong class="">Step ${i}:</strong>
                    </div>
                    <div class="div col s10">
                        <textarea id="step_${i}" name="step[]" minlength="5" class="materialize-textarea validate required"></textarea>
                    </div>
                </div>`
    $('.steps').append(html);
});
