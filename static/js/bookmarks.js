$(document).ready(function () {
            // Обработчик клика на элементе li
            $('.ajax-list').on('click', 'li', function () {
                // Удаляем класс selected у всех элементов
                $(this).closest('ul').find('li').removeClass('selected');

                var pageName = $(this).data('page');
                // Получаем значение переменной max_dsc из атрибута data
                var maxDscValue = $(this).data('max-dsc');

                // Используем извлеченное значение max_dsc в AJAX-запросе
                $.ajax({
                    url: "/static/includes/" + pageName,
                    data: { max_dsc: maxDscValue },
                    cache: false,
                    success: function (html) {
                        $("#content").html(html);
                        // Устанавливаем значение src для элемента iframe
                        $('#max_dsc_iframe').attr('src', maxDscValue);
                    }
                });

                // Добавляем класс selected к выбранному элементу
                $(this).addClass('selected');
            });
        }); 