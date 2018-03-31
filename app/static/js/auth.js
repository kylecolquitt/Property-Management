function checkPasswordMatch() {
    $("#submitButton").prop("disabled", true);
    
    var password = $('.passwordField').val();
    var confirmPassword = $("#txtConfirmPassword").val();

    if (password != confirmPassword){
        $("#divCheckPasswordMatch").html("Passwords do not match!");
    }
    else{
        $(":submit").attr("disabled", false);
        
        $("#divCheckPasswordMatch").html("Passwords match.");
    }
}

$(document).ready(function () {
   $("#txtConfirmPassword").keyup(checkPasswordMatch);
});