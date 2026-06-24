// Когда HTML-документ полностью загружен и DOM готов к работе
$(document).ready(function () {
    // Сохраняем в переменную элемент для отображения уведомлений от AJAX-запросов
    var successMessage = $("#jq-notification");

    // Обработчик клика по кнопке "Добавить в корзину"
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault(); // Отменяем стандартное действие ссылки

        // Получаем текущий счетчик товаров в корзине и преобразуем в число
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id товара из data-атрибута кнопки
        var product_id = $(this).data("product-id");

        // Получаем URL для добавления товара в корзину из атрибута href
        var add_to_cart_url = $(this).attr("href");

        // Отправляем POST-запрос через AJAX для добавления товара в корзину
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),  // CSRF токен для безопасности
            },
            success: function (data) {
                // Показываем сообщение об успешном добавлении товара
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7 секунд скрываем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Увеличиваем счетчик товаров в корзине на 1
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Обновляем содержимое корзины на странице новым HTML от сервера
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function () {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    // Обработчик клика по кнопке "Удалить товар из корзины"
    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault(); // Отменяем стандартное действие ссылки

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id элемента корзины из data-атрибута
        var cart_id = $(this).data("cart-id");
        // Получаем URL для удаления товара из корзины
        var remove_from_cart = $(this).attr("href");

        // Отправляем POST-запрос на удаление товара
        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Показываем сообщение об успешном удалении
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Уменьшаем счетчик товаров на количество удаленных позиций
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Обновляем содержимое корзины новым HTML
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function () {
                console.log("Ошибка при удалении товара из корзины");
            },
        });
    });

    // Обработчик клика по кнопке уменьшения количества товара
    $(document).on("click", ".decrement", function () {
        // Получаем URL для изменения количества товара
        var url = $(this).data("cart-change-url");
        // Получаем id корзины
        var cartID = $(this).data("cart-id");
        // Ищем input с количеством рядом с кнопкой
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());

        // Если количество больше 1, уменьшаем на 1 и обновляем корзину
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик клика по кнопке увеличения количества товара
    $(document).on("click", ".increment", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());

        // Увеличиваем количество на 1 и обновляем корзину
        $input.val(currentValue + 1);
        updateCart(cartID, currentValue + 1, 1, url);
    });

    // Функция для отправки AJAX-запроса на сервер для обновления количества товара в корзине
    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Отображаем сообщение от сервера
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Обновляем счетчик товаров в корзине с учетом изменения
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Обновляем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function () {
                console.log("Ошибка при обновлении количества товара в корзине");
            },
        });
    }

    // Автоматическое скрытие уведомления от Django через 7 секунд, если оно есть
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    // При клике на иконку корзины открываем модальное окно с корзиной
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');  // Перемещаем модальное окно в body (чтобы работало корректно)
        $('#exampleModal').modal('show');    // Показываем модальное окно
    });

    // Закрытие модального окна корзины по клику на кнопку закрытия
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    // Обработчик изменения выбора способа доставки (радиокнопки)
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        // Если выбран вариант "требуется доставка" (значение "1"), показываем поле для ввода адреса
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            // Иначе скрываем поле адреса доставки
            $("#deliveryAddressField").hide();
        }
    });

    // Форматирование поля ввода номера телефона в режиме реального времени
    document.getElementById('id_phone_number').addEventListener('input', function (e) {
        // Убираем все символы кроме цифр
        var digits = e.target.value.replace(/\D/g, '');

        // Ограничиваем длину до 12 цифр (код страны + номер)
        if (digits.length > 12) digits = digits.substring(0, 12);

        var formatted = '';

        // Форматируем номер, если он начинается с кода страны 375 (Беларусь)
        if (digits.startsWith('375')) {
            var rest = digits.substring(3);
            formatted = '375';

            if (rest.length > 0) {
                formatted += '-(' + rest.substring(0, Math.min(2, rest.length));
            }
            if (rest.length >= 2) {
                formatted += ')';
            }
            if (rest.length > 2) {
                formatted += '-' + rest.substring(2, Math.min(5, rest.length));
            }
            if (rest.length > 5) {
                formatted += '-' + rest.substring(5, Math.min(7, rest.length));
            }
            if (rest.length > 7) {
                formatted += '-' + rest.substring(7, Math.min(9, rest.length));
            }
        } else {
            // Если номер не начинается с 375 — выводим только цифры без форматирования
            formatted = digits;
        }

        // Обновляем поле ввода отформатированным номером
        e.target.value = formatted;
    });

    // Валидация формы оформления заказа при отправке
    $('#create_order_form').on('submit', function (event) {
        var phoneNumber = $('#id_phone_number').val();
        // Регулярное выражение для проверки формата: 375-(xx)-xxx-xx-xx
        var regex = /^375-\(\d{2}\)-\d{3}-\d{2}-\d{2}$/;

        if (!regex.test(phoneNumber)) {
            // Если формат не соответствует, показываем ошибку и отменяем отправку формы
            $('#phone_number_error').show();
            event.preventDefault();
        } else {
            // Если формат корректный, скрываем ошибку
            $('#phone_number_error').hide();
            // Очищаем номер от скобок, дефисов и пробелов перед отправкой на сервер
            var cleanedPhoneNumber = phoneNumber.replace(/[()\-\s]/g, '');
            $('#id_phone_number').val(cleanedPhoneNumber);
        }
    });
});
