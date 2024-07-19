

async function amount_pressed(pk,action) {
var x = document.getElementById('amount_' + pk)


if (!(action === 'minus' && x.innerHTML < 1)) {
        try {
        const response = await fetch('ajax?' + 'pk=' + pk + '&action='+ action, {
            method: 'GET'
        });
        if (response.ok) {
            if (action == 'plus') {
                x.innerHTML ++
            }
            else if (action == 'minus') {x.innerHTML --}
            else {x.innerHTML = '0'}
            const result = await response.json();


            document.getElementById('total-price').innerHTML = 'итог: $' + Number(result['total_price'])
            console.log(result);

            var new_cost = result['new_cost']
            const new_cost_with_discount = result['new_cost_with_discount']

            if (new_cost_with_discount == new_cost) {  new_cost = ''}
            else {new_cost = '$' + new_cost}
            console.log(new_cost);
            const amount = result['amount']
            const name = result['name']

            const is_created_or_deleted = result['is_created_or_deleted']
            if (is_created_or_deleted) {
                if (action == 'plus') {
                    const cart = document.getElementById('cart-purchases')
                    const cartHtml = `
                        <div class="cart-item" id="cart-item-id-${pk}">

                            <button class="cart-item-delete" onclick="amount_pressed(${pk}, 'delete')">X</button>
                            <p class="cart-item-name">
                                ${name} (<span id="cart-item-name-id-${pk}">${amount}</span> шт.)
                            </p>
                            <s class="price-without-discount" id="cart-price-without-discount-${pk}">${new_cost}</s>
                            <h4 class="cart-item-price" id="cart-price-id-${pk}">
                                $${new_cost_with_discount}
                            </h4>
                        </div>`;
                    cart.insertAdjacentHTML('beforeend', cartHtml)
                    }
                else {
                    document.getElementById('cart-item-id-' + pk).remove()
                }

            }
            else {

            document.getElementById('cart-price-id-' + pk).innerHTML = '$' + new_cost_with_discount
            document.getElementById('cart-item-name-id-' + pk).innerHTML = amount
            document.getElementById('cart-price-without-discount-' + pk).innerHTML =  new_cost
            }

      }

         else {
            console.error('Ошибка сети:', response.statusText);
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}
}



