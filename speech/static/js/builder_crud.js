function addPhrase(){
    var one = $('.row.first.template').clone(true);
    var two = $('.row.second.template').clone(true);
    var div = $('.divider.template').clone(true);

    one = one.removeClass('template');
    two = two.removeClass('template');
    div = div.removeClass('template');

    var num_primary = parseInt($('#id_num_primary_keywords').val());
    one.find('input').first().attr('name', 'primary_keyword_field_' + num_primary);
    one.find('input').eq(1).attr('name', 'primary_keyword_point_field_' + num_primary);
    two.find('input').first().attr('name', 'primary_keyword_hint_field_' + num_primary);

    $('#phraseArea').append(one, two, div);

    $('#id_num_primary_keywords').val(num_primary + 1);
}

function addImage() {
    var numImages = parseInt($('#numImages').val());
    var imgRow = $('.url.template').clone(true);
    imgRow.removeClass('template');
    imgRow.find('input').attr('name', 'img_' + numImages);
    $('#urlContainer').append(imgRow);
    $('#numImages').val(numImages + 1);
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

    $(document).on('click','#addImage',function(){
        addImage();
    });

    updateDOM();

});
