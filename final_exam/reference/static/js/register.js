var email = document.getElementById("id_email");
email.onblur = function () {
    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var email_str = email.value;
    if (!reg.test(email_str)) {
        document.getElementById("error_show").innerHTML = "Invalid email!";
    } else {
        document.getElementById("error_show").innerHTML = "";
    }
};

var psw1 = document.getElementById("id_password");
var psw2 = document.getElementById("id_password_confirmation");

psw1.onblur = psw2.onblur = function () {
    if (psw1.value.length < 6 || psw2.value.length < 6) {
        document.getElementById("psw_error").innerHTML = "Password too short (6 chars. min)";
    } else {
        document.getElementById("psw_error").innerHTML = "";
    }
    if (psw1.value != psw2.value) {
        document.getElementById("psw_match").innerHTML = "Password mismatch!";
    } else {
        document.getElementById("psw_match").innerHTML = "";
    }
};

function validation() {
    var is_valid = true;

    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var email = document.getElementById("id_email").value;
    if (!reg.test(email)) {
        document.getElementById("error_show").innerHTML = "Invalid email!";
        return false;
    }

    var psw1_str = document.getElementById("id_password").value;
    var psw2_str = document.getElementById("id_password_confirmation").value;
    if (psw1_str.length < 6 || psw2_str.length < 6) {
        document.getElementById("psw_error").innerHTML = "Password too short (6 chars. min)";
        return false;
    }
    if (psw1_str !== psw2_str) {
        document.getElementById("psw_match").innerHTML = "Password mismatch!";
        return false;
    }

    return true;
}