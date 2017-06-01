function addPhrase(){
    var cloned = $('.row').eq(1).clone(true);

    $('#phraseArea').append(cloned);

    var num_primary = parseInt($('#id_num_primary_keywords').val());
    $('#id_num_primary_keywords').val(num_primary + 1);
}

function updateDOM() {
    $('.removephrase').on('click', function(){
       var num_primary = parseInt($('#id_num_primary_keywords').val());
       if (num_primary != 1) {
           $('#id_num_primary_keywords').val(num_primary - 1);
           $(this).closest('.row').remove();
           updateValues();
       }
    });

    $('.removesyn').on('click', function (){
        $(this).closest('.syn').remove();
    })

    $('.addsyn').on('click', function(){
        $(this).css('display', 'none');
        $(this).prev().css('display', 'inline');
    })

    $(document).keypress(function(e) {
        if(e.which == 13 && $(':focus').parent().hasClass('syninput')){
            var text = $(':focus').val();
            text = text.replace(/[^a-zA-Z0-9 ]/g, '');

            var add = $(':focus').parent().next();

            if (text != '') {
                htmlToAdd = '<button class="ui basic icon button syn" style="margin-top: 3px" type="button">' + text +
                    '<i class="icon remove removesyn"></i></button>';
                $(':focus').parent().prev().after(htmlToAdd);
            }

            add.css('display','inline');
            $(':focus').val('');
            $(':focus').parent().css('display', 'none');

            updateDOM();
        }

        if(e.which == 13){
            e.preventDefault();
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
