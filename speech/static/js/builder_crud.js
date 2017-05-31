function addPhrase(){
    var cloned = document.getElementsByClassName("row")[1].cloneNode(true);

    var addHtml = "<div class='row'>" + cloned.innerHTML + "</div>";
    var newHtml = $('#phraseArea').html() + addHtml;
    $('#phraseArea').html(newHtml)

    var num_primary = parseInt($('#id_num_primary_keywords').val());
    $('#id_num_primary_keywords').val(num_primary + 1);
}

function updateDOM() {
    $('.remove').on('click', function(){
       var num_primary = parseInt($('#id_num_primary_keywords').val());
       if (num_primary != 1) {
           $('#id_num_primary_keywords').val(num_primary - 1);
           $(this).closest('.row').remove();
           updateValues();
       }
    });
}

$(document).ready(function(){
    $(document).on('click','#addPhrase',function(){
        addPhrase();
        updateValues();
        updateDOM();
    });

    updateDOM();

});
