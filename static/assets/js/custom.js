let count = localStorage.getItem('shoppingCartCount') || 0;
let cartCountElem = document.getElementById("cart-count");
cartCountElem.innerHTML = count;

function addtocart(button){
    var fruitId = button.parentNode.querySelector('input[name="fruit_id"]').value;
    $.ajax({
    type: "POST",
    url: "/fruit/",
    data: { 'fruit_id': fruitId,'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
    success: function (data) {
        console.log(data)
        $.toast({
            text: 'Successfully added!',
            showHideTransition: 'fade',
            icon: 'success',
            position: 'top-right',
            bgColor: '#28a745',
            textColor: '#ffffff',
            allowToastClose: true,
            hideAfter: 5000
        });

        cartCountElem.innerHTML = data.quantity;
        localStorage.setItem('shoppingCartCount', data.quantity);
        
    },
    error: function(response){
        console.log(response);
        $.toast({
            text: 'Erro!',
            showHideTransition: 'fade',
            icon: 'error',
            position: 'top-right',
            bgColor: '#28a745',
            textColor: '#ffffff',
            allowToastClose: true,
            hideAfter: 5000
        });
    }
});
};


function updateTotal(input) {
    var row = input.closest('.table-body-row');

    var id = row.dataset['productId']

    var quantity = input.value;
    
    var price = parseFloat(row.querySelector('.product-price').innerText.substring(1));
    
    var total = price * quantity;

    $.ajax({
        type: "POST",
        url: "/cart-update/",
        data: {'cart_id':id,"total":total,"quantity":quantity,'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
        success: function (data) {
            row.querySelector('.product-total').innerText = total;
            cartCountElem.innerHTML = data.quantity;
            localStorage.setItem('shoppingCartCount', data.quantity);
    
        },
        error: function(response){
            console.log(response);
        }
    });
}

function removeProduct(button) {
    var row = button.closest('.table-body-row');
    cart_id = row.dataset['productId']
    $.ajax({
        type: "POST",
        url: "/cart-delete/",
        data: {'cart_id':cart_id,'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
        success: function (data) {
            row.remove();
            $.toast({
                text: 'Product removed successfully',
                showHideTransition: 'fade',
                icon: 'success',
                position: 'top-right',
                bgColor: '#28a745',
                textColor: '#ffffff',
                allowToastClose: true,
                hideAfter: 5000
            });
            cartCountElem.innerHTML = data.quantity;
            localStorage.setItem('shoppingCartCount', data.quantity);
    
        },
        error: function(response){
            console.log(response);
        }
    });
}


function ContactusForm() {
    let name = $("#name").val();
    let email = $("#email").val();
    let phone = $("#phone").val();
    let subject = $("#subject").val();
    let message = $("#message").val();

    $.ajax({
        type: "POST",
        url: "/contact_form/",
        data: {'name':name,'email':email,'phone':phone,'subject':subject,'message':message,'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
        success: function (data) {
            debugger
            if (data.msg != 'error'){
                $.toast({
                    text: 'Your Application Submit!',
                    showHideTransition: 'fade',
                    icon: 'success',
                    position: 'top-right',
                    bgColor: '#28a745',
                    textColor: '#ffffff',
                    allowToastClose: true,
                    hideAfter: 5000
                });
                document.getElementById("fruitkha-contact").reset();
            }
            else{
                alert("Fill the form")
            }
        },
        error: function(response){
            console.log(response);
        }
    });
}