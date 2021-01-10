let i = 3

$(document).ready(function(){
    $('.sidenav').sidenav({edge: "top"});

    $('select').formSelect();

    $(this).on("click", "#add_new_step", function() {
        i++;
        let stepHTML = `<div class="row step">
                            <div class="input-field col s12 m2 center">
                                <strong class="">Step ${i}:</strong>
                            </div>
                            <div class="col s9 offset-s1 m9">
                                <textarea id="step_${i}" name="step[]" minlength="5" required class="materialize-textarea validate"></textarea>
                            </div>
                            <div class="col s1 m1 center">
                                    <button type="button" id="delete_step" class="btn pink lighten-4 black-text text-shadow ">
                                        <i class="far fa-times-circle"></i>
                                    </button>
                                </div>
                        </div>`
        $('.steps').append(stepHTML);
    });

    $(this).on("click", "#add_new_ingredient", function() {
        let ingredientHTML = `<div class="row">
                                <div class="input-field col s12 m2 center">
                                    <strong class="">Ingredient:</strong>
                                </div>
                                <div class="col s9 offset-s1 m3">
                                    <textarea id="ingredients" name="ingredients[]" required class="materialize-textarea validate"></textarea>
                                </div>
                                <div class="col s1 m1 center">
                                    <button type="button" id="delete_ingredient" class="btn pink lighten-4 black-text text-shadow ">
                                        <i class="far fa-times-circle"></i>
                                    </button>
                                </div>
                            </div>`;
        $('.ingredients').append(ingredientHTML);
    })

    $(this).on("click", "#delete_step", function() {
        i--
        let deleteInput = $(this).parent().parent();
        deleteInput.remove()
        // code to make i = +1 of last step
    })

    $(this).on("click", "#go_back", function() {
        window.history.back();
    })

    $(this).on("click", "#delete_ingredient", function() {
        let deleteInput = $(this).parent().parent();
        deleteInput.remove()
    })
    $('#manage').on("click", function() {
        $('.hidden').toggle();
    })
});