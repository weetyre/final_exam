var email = document.getElementById("id_text");

function emailValidation() {
    var reg = /@/;
    var email_s = email.value;
    if (reg.test(email_s)) {
        var regs = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
        var email_str = email.value;
        if (!regs.test(email_str)) {
            document.getElementById("error_show").innerHTML = "enter a valid email address.";
            return false;
        } else {
            document.getElementById("error_show").innerHTML = "";
            return true;
        }
    } else {
        document.getElementById("error_show").innerHTML = "";
        return true;
    }


}

email.onblur = function () {
    emailValidation()
};