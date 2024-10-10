$(document).ready(function () {
        // Обработка нажатия на кнопку "Задать вопрос" с делегированием событий
        $(document).on('click', '#openModalButton', function (event) {
                event.preventDefault(); // Предотвращаем переход по ссылке

                // Открываем модальное окно
                $('#modal1').modal('show');

                // Загружаем форму в модальное окно с помощью AJAX через Flask
                $('#modalContent').load('/question', function () {
                    console.log('Форма загружена');
                    // Скрипт для отправки формы AJAX, как только форма будет загружена
                    $('#questionForm').submit(function (event) {
                        event.preventDefault(); // Предотвращаем перезагрузку страницы

                        var formData = $(this).serialize(); // Собираем данные формы
                        console.log('Форма отправляется: ' + formData);

                        $.ajax({
                            url: '/send_email',
                            type: 'POST',
                            data: formData,
                            success: function (response) {
                                alert('Форма успешно отправлена!');
                                $('#modal1').modal('hide');
                            },
                            error: function (xhr, status, error) {
                                console.error('Ошибка при отправке: ' + status + ' ' + error);
                                alert('Произошла ошибка при отправке формы');
                            }
                        });
                    });
                });
            });
        });
