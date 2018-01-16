$( document ).ready(function() {
    $.ajax({
        method: "get",
        url: "/cup-of-coffee/",
        success: function (data) {
            var obj = $.parseJSON(data);
            $('#coffee_cups').text(obj.cups)
        }
    })
    function endOfTheGame (company) {
        $.ajax({
            method: "POST",
            url: "/choose-company/",
            data: { company: company, csrfmiddlewaretoken: $.cookie("csrftoken")},
            success: function (data) {
                var obj = $.parseJSON(data);
                $('.wrapper').html(obj.html)
                var $progressBar = $('.progress-bar')
                if (obj['status'] === 'lose' || obj['status'] === 'send-cv') {
                    $progressBar.css('width', '100%').addClass('bg-danger').text('')
                } else if (obj['status'] === 'win') {
                    $progressBar.css('width', '100%').addClass('bg-success').text('100%')
                } else if (obj['status'] === 'not so bad') {
                    $progressBar.css('width', '80%').addClass('bg-success').text('80%')
                }
            }
        })
    }
    $('.companies a').on('click', function(e) {
        e.preventDefault()
        endOfTheGame($(this).data('val'))
    })

    $('#send_cv').on('click', function (e) {
        e.preventDefault()
        endOfTheGame(4)
    })

    $('#frontend').on('click', function (e) {
        e.preventDefault()
        endOfTheGame(1)
    })

    var buttons = document.getElementById("buttons");
    if (buttons) {
        for (var i = buttons.children.length; i >= 0; i--) {
            buttons.appendChild(buttons.children[Math.random() * i | 0]);
        }
    }

    $('#gender_selected').attr('disabled', 'disabled')
    $('#gender_form').change(function() {
        if ($("input[name='gender']").is(':checked')) {
            $('#gender_selected').attr('disabled', false)
        }
    })

    $('#coffee').on('click', function (e) {
        if (localStorage.getItem('coffee')) {
            var coffee = localStorage.getItem('coffee')
            coffee++
            localStorage.setItem('coffee', coffee)
        } else {
            localStorage.setItem('coffee', 0)
        }
        swal({
            title: 'Drinking!',
            imageUrl: 'https://media.giphy.com/media/xT9IgMVeZBLP1s3doQ/giphy.gif',
            imageWidth: 480,
            imageHeight: 480,
            timer: 2000,
            showConfirmButton: false,
            animation: false,
            onOpen: function () {
                $.ajax({
                    method: "POST",
                    url: "/cup-of-coffee/",
                    data: { value: 1, csrfmiddlewaretoken: $.cookie("csrftoken")},
                    success: function (data) {
                        var obj = $.parseJSON(data);
                        $('#coffee_cups').text(obj.cups)
                    }
                })
            }
        })
    })
    $('#wait').on('click', function (e) {
        var $progressBar = $('.progress-bar')
        $progressBar.css('width', '45%').addClass('bg-success').text('45%')
        swal({
            title: '<i class="fa fa-refresh fa-spin fa-3x" aria-hidden="true"></i>',
            text: 'Half a year passed,  promised project never appeared, feeling deceived, need to start everything from the beginning :(',
            timer: 5000,
            showConfirmButton: false,
            onOpen: function () {
                setTimeout(function () { $progressBar.css('width', '100%').addClass('bg-danger').text('') }, 2000);
            },
            onClose: function () {
                window.location.replace("/start/");
            }
        })
    })
});