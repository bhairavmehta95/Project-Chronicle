function updateValues(){
    var pointList = $('.points').find('input');
    var totalPoints = 0;
    for (i =0; i < pointList.length; ++i){
        totalPoints += parseInt(pointList[i].value);
    }

    $('.progress').each(function(index) {
        var progress = pointList[index].value / totalPoints * 100;
        var intProgress = Math.round( progress );

        $(this).progress({
            percent: intProgress
        });
    });

}

$(document).ready(function() {
    updateValues();

    $('.points').change(function() {
        updateValues();
    });

});



