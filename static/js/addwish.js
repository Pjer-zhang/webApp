/**
 * Created by pjer on 2016/7/2.
 */
	/**$(function(){
		$.ajax({
			url : '/getWish',
			type : 'GET',
			success: function(res){
				var div = $('<div>')
    .attr('class', 'list-group')
    .append($('<a>')
        .attr('class', 'list-group-item active')
        .append($('<h4>')
            .attr('class', 'list-group-item-heading'),
            $('<p>')
            .attr('class', 'list-group-item-text')));
							    
				
				
				var wishObj = JSON.parse(res);
				var wish = '';
				
				$.each(wishObj,function(index, value){
					wish = $(div).clone();
					$(wish).find('h4').text(value.Title);
					$(wish).find('p').text(value.Description);
					$('#wishlist').append(wish);
				});
			},
			error: function(error){
				console.log(error);
			}
		});
	}); **/

    







	$(function(){

		GetWishes();
		$('#btnUpdate').click(function(){
			$.ajax({
			url : '/updateWish',
			data : {title:$('#editTitle').val(),description:$('#editDescription').val(),id:localStorage.getItem('editId')},
			type : 'POST',
			success: function(res){

			$('#editModal').modal('hide');

				GetWishes();



			},
			error: function(error){
				console.log(error);
			}
		});
		});
	});
	function GetWishes(){
		$.ajax({
			url : '/getWish',
			type : 'GET',
			success: function(res){




				var wishObj = JSON.parse(res);
				$('#ulist').empty();
				$('#listTemplate').tmpl(wishObj).appendTo('#ulist');

			},
			error: function(error){
				console.log(error);
			}
		});
	}
	function ConfirmDelete(elem){
		localStorage.setItem('deleteId',$(elem).attr('data-id'));
		$('#deleteModal').modal();
	}
	function Delete(){
		$.ajax({
			url : '/deleteWish',
			data : {id:localStorage.getItem('deleteId')},
			type : 'POST',
			success: function(res){
				var result = JSON.parse(res);
				if(result.status == 'OK'){
					$('#deleteModal').modal('hide');
					GetWishes();
				}
				else{
					alert(result.status);
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	}

    function Edit(elm){
		localStorage.setItem('editId',$(elm).attr('data-id'));
		$.ajax({
			url : '/getWishById',
			data : {id:$(elm).attr('data-id')},
			type : 'POST',
			success: function(res){

				var data = JSON.parse(res);
				$('#editTitle').val(data[0]['Title']);
				$('#editDescription').val(data[0]['Description']);
				$('#editModal').modal();



			},
			error: function(error){
				console.log(error);
			}
		});
	}