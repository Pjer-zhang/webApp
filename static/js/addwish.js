/**
 * Created by pjer on 2016/7/2.
 */
	/**   **/

	

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





function Edithave(elm){
		localStorage.setItem('editId',$(elm).attr('data-id'));
		$.ajax({
			url : '/getHave',
			success: function(res){

				var data = JSON.parse(res);
				$('#editTitle_have').val(data['ihavenum']);
				$('#editDescription_have').val(data['ihavedes']);
				$('#editModal_have').modal();

			},
			error: function(error){
				console.log(error);
			}
		});
	}

$(function(){

		Gethave();
		$('#btnUpdate_have').click(function(){
			$.ajax({
			url : '/updateHave',
			data : {title:$('#editTitle_have').val(),description:$('#editDescription_have').val(),id:localStorage.getItem('editId')},
			type : 'POST',
			success: function(res){
			$('#editModal_have').modal('hide');
				Gethave();
			},
			error: function(error){
				console.log(error);
			}
		});
		});
	});

function Gethave(){
		$.ajax({
			url : '/getHave',
			type : 'GET',
			success: function(res){
				var datares = JSON.parse(res);
                $('#ihavenum').replaceWith("<h2 class=\"list-group-item-heading\"id=\"ihavenum\">" + datares['ihavenum'] + "</h2>")
                $('#ihavedes').replaceWith("<p class=\"list-group-item-text\" id=\"ihavedes\">"+datares['ihavedes']+"</p>")

			},
			error: function(error){
				console.log(error);
			}
		});
	}

