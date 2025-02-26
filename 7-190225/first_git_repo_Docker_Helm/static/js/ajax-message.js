$(document).ready(function() {
    $('#contact-form').on('submit', function(event) {
        event.preventDefault(); // Предотвращаем перезагрузку страницы
        $.ajax({
            url: '/send_message',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                $('.message').html('<div class="success">' + response.success + '</div>').fadeIn().delay(3000).fadeOut();
            },
            error: function(xhr) {
                $('.message').html('<div class="error">' + xhr.responseJSON.error + '</div>').fadeIn().delay(3000).fadeOut();
            }
        });
    });
});