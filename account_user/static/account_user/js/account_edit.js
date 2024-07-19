document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('chooseAvatarButton').addEventListener('click', function() {
        document.getElementById('avatarInput').click();
    });

    document.getElementById('avatarInput').addEventListener('change', function() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('avatarPreview').src = e.target.result;
            };
            reader.readAsDataURL(input.files[0]);
        }
    });



    document.getElementById('back_but').addEventListener('click', function() {
        document.getElementById('pass_win').style.display = 'none';
    });

async function checkForm(event) {
    event.preventDefault();  // Предотвращаем отправку формы по умолчанию

    var value = document.getElementById('id_password_valid').value;
    try {
        const response = await fetch('ajax?' + 'passw=' + value, {
            method: 'GET'
        });

        if (response.ok) {
            const result = await response.json();
            console.log(result);

            if (result['validate']) {
                event.target.submit();  // Отправляем форму вручную
            } else {
                document.getElementById('id_password_valid').value = ''
                document.getElementById('pass_er').innerHTML = 'пароль введен неверно'
            }
        } else {
            console.error('Ошибка сети:', response.statusText);
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

    // Привязываем обработчик события отправки формы
    document.querySelector('form').addEventListener('submit', checkForm);
});

function win_show() {
    document.getElementById('pass_win').style.display = 'block';
}