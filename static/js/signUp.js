function fadeAlert() {
        window.setTimeout(function() {
            $(".alert").fadeTo(1500, 0).slideUp(500, function() {
                $(this).remove();
            });
        }, 1000);
    }


$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response) {
                res = JSON.parse(response);
                if (res.hasOwnProperty('message')) {
                $('#msgs').html("<div class='alert alert-success'>" + res.message + "</div>");
                    fadeAlert();
                    window.location.replace("/showSignin");
                }
                else if (res.hasOwnProperty('error')) {
                $('#msgs').html("<div class='alert alert-danger'>" + res.error.substring(3,res.error.length-3) + "</div>");
                fadeAlert();
                }
            },
			error: function(error){
				$('#msgs').html("<div class='alert alert-danger'>"+error+"</div>");
			}
		});
	});
});


