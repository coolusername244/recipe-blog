  let i = 5

  $(document).ready(function(){
    $('.sidenav').sidenav({edge: "top"});
    $('select').formSelect();
    $('#add_new').on("click", function(){
        i++;
        let html = `<div class="row step">
                        <div class="input-field col s2 center">
                            <strong class="">Step ${i}:</strong>
                        </div>
                        <div class="div col s10">
                            <textarea id="step_${i}" name="step_${i}" minlength="5" class="materialize-textarea validate required"></textarea>
                            <label for="step_${i}"></label>
                        </div>
                    </div>`
        $('.steps').append(html);
    });
  });