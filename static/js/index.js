

$(function(){
var div = $('<div>')
    .attr('class', 'list-group')
    .append($('<a>')
        .attr('class', 'list-group-item col-xs-3').attr('style','width:140px;margin:5px')
        .append($('<h4>')
            .attr('class', 'list-group-item-heading'),
            $('<p>')
            .attr('class', 'list-group-item-text')));

		$.ajax({
			url : '/getAllWish',
			type : 'GET',
			success: function(res){
                var wishObj = JSON.parse(res);
				var wish = '';
				
				$.each(wishObj,function(index, value){
					wish = $(div).clone();
					$(wish).find('h4').text(value.num);
					$(wish).find('p').text(value.name);
					$(wish).find('a').attr('class','list-group-item active col-xs-3')
                    $('#numList').append(wish);
				});
			},
			error: function(error){
				console.log(error);
			}
		});

        $.ajax({
			url : '/getAllHave',
			type : 'GET',
			success: function(res){
				var wishObj = JSON.parse(res);
				var wish = '';

				$.each(wishObj,function(index, value){
					wish = $(div).clone();
					$(wish).find('h4').text(value.num);
					$(wish).find('p').text(value.name);
					$('#haveList').append(wish);
				});
			},
			error: function(error){
				console.log(error);
			}
		});




	});




/**
 * Created by pjer on 2016/6/11.
 */
