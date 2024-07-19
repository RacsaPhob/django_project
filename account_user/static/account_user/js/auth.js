
function checkForm(form) {
    var error = ''
    var username = document.getElementById('id_username');
    var pass = document.getElementById('id_password1').value;
    var pass1 = document.getElementById('id_password2').value;
    var errorusername = document.getElementById('usernameError');
    var errorpassword = document.getElementById('password1Error')

    if (username.value.length <=3 || username.value.length >= 25) {
        error = 'неккоректная длина имени';
        errorusername.innerHTML = error;
        }
    else if (pass.length <= 6) {
        error = 'длина пароля должна быть более 6 символов'
    }
    else if (pass != pass1) {
        error = 'пароли не совпадают'
    }
    errorpassword.innerHTML = error

    console.log(error)
    if (error) {
        return false
    }
    return true;
}

function google_pressed () {

    window.location.href = 'google'
}
