function cat_pressed(cat) {
    var menu = document.getElementById('menu-content');
    menu.innerHTML = ''; // Очистка текущих элементов

    fetch('ajax?' + 'cat=' + encodeURIComponent(cat), {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {

            data.items.forEach(item => {
                const menuItem = document.createElement('div');
                const menuImage = document.createElement('img');
                const menuName = document.createElement('h2')
                const menuPrice = document.createElement('p')
                const menuLink = document.createElement('a')

                menuImage.classList.add('menu_image');
                menuImage.src = item.image;
                menuName.textContent = item.name
                menuPrice.textContent = '$' + item.price
                menuLink.href = item.link + '?prev=' + cat

                menuLink.appendChild(menuName)


                menuItem.classList.add('menu-item');
                menuItem.id = `menu-item-${item.id}`;
                menuItem.appendChild(menuImage);
                menuItem.appendChild(menuLink);
                menuItem.appendChild(menuPrice);



                menu.appendChild(menuItem)

            });
        })
        .catch(error => console.error('Ошибка:', error));
}
