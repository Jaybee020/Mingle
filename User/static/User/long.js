$(document).ready(function(){
	$('.menu-but').click(function(){
		if ($('.nav-links').width() > 0) {
			$('.nav-links').animate({width: '0px'}, 700);
		}else {
			$('.nav-links').animate({width: '340px'}, 700);
		}
	});

	var $divs = $("div.person");

	$('#numBnt').on('click', function () {
	    var numericallyOrderedDivs = $divs.sort(function (a, b) {
	    	get1 = $(a).find(".mes-time").text();
	    	time1 = parseInt(get1[0] * 10) + parseInt(get1[1]);
	    	time2 = parseInt(get1[3] * 10) + parseInt(get1[4]);
			secs1 = (time1 * 3600)+(time2 * 60);

			get2 = $(b).find(".mes-time").text();
	    	time3 = parseInt(get2[0] * 10) + parseInt(get2[1]);
	    	time4 = parseInt(get2[3] * 10) + parseInt(get2[4]);
			secs2 = (time3 * 3600)+(time4 * 60);

	        return  secs1 - secs2;
	    });

	    $(".recent").html(numericallyOrderedDivs);
	});


});