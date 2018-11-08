var email = document.getElementById("id_email");
email.onblur = function () {
    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var email_str = email.value;
    if (!reg.test(email_str)) {
        document.getElementById("error_show").innerHTML = "enter a valid email address.";
    } else {
        document.getElementById("error_show").innerHTML = "";
    }
};

var psw1 = document.getElementById("id_password");
var psw2 = document.getElementById("id_password_confirmation");

psw1.onblur = psw2.onblur = function () {
    if (psw1.value.length < 6 || psw2.value.length < 6) {
        document.getElementById("psw_error").innerHTML = "password too short.";
    } else {
        document.getElementById("psw_error").innerHTML = "";
    }
    if (psw1.value != psw2.value) {
        document.getElementById("psw_match").innerHTML = "password mismatch!";
    } else {
        document.getElementById("psw_match").innerHTML = "";
    }
};


 var username = document.getElementById("id_username");
 username.onblur = function () {
      var reg2 =/^[a-z]+$/;
      var username_value = username.value;
      if (!reg2.test(username_value)) {
        document.getElementById("name_error").innerHTML = "username has illegal characters.";
      }else {
        document.getElementById("name_error").innerHTML = "";
      }
 }


function validation() {
    var is_valid = true;

    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var email = document.getElementById("id_email").value;
    if (!reg.test(email)) {
        document.getElementById("error_show").innerHTML = "enter a valid email address.";
        return false;
    }

    var psw1_str = document.getElementById("id_password").value;
    var psw2_str = document.getElementById("id_password_confirmation").value;
    if (psw1_str.length < 6 || psw2_str.length < 6) {
        document.getElementById("psw_error").innerHTML = "password too short.";
        return false;
    }
    if (psw1_str !== psw2_str) {
        document.getElementById("psw_match").innerHTML = "password mismatch.";
        return false;
    }

    //用户名验证
    var reg2 =/^[a-z]+$/;
    var username = document.getElementById("id_username").value;

    if (!reg2.test(username)) {
        document.getElementById("name_error").innerHTML = "username has illegal characters.";
        return false;
    }
}