(function(){
    // using jQuery, Django post request, code from django documents
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $('#create-option').on('click', function(){
        $('.option').each(function(){
            $(this).val('');
            $(this).attr('disabled', false);
        });
        $('#save-option').css('display', 'none');
        $('#submit-option').css('display', 'block');
        $('#cancel').css('display', 'block');
    });


    $('#submit-option').on('click', function(){
        var optionsName = $('#options-name').val(),
            keyword = $('#keyword').val(),
            delay = $('#download-delay').val(),
            beginPage = $('#begin-page-num').val(),
            endPage = $('#end-page-num').val(),
            t_wm = $('#_T_WM').val(),
            suhb = $('#SUHB').val(),
            sub = $('#SUB').val(),
            gsid_CTandWM = $('#gsid_CTandWM').val(),
            user_id = $("#user").attr('index');
        $.ajax({
            url: '/create_options/',
            type: 'POST',
            data: {
                'optionsName': optionsName,
                'keyword': keyword,
                'delay': delay,
                'beginPage': beginPage,
                'endPage': endPage,
                't_wm': t_wm,
                'suhb': suhb,
                'sub': sub,
                'gsid_CTandWM': gsid_CTandWM,
                'user_id': user_id
            },
            success: function(response){
                if( response === 'True' ){
                    $('#msg').html('');
                    $('#msg').append('<p>Save Success!</p>');
                    $('#msg-modal').modal('show');
                    setTimeout(function(){
                        window.location.reload();
                    }, 1000);
                }else{
                    $('#msg').html('');
                    $('#msg').append('<p>Save Fail!</p>');
                    $('#msg-modal').modal('show');
                }
                
            }
        });

    });

    $('#get-option').on('click', function(){
        $.ajax({
            url: '/get_options/',
            type: 'POST',
            dataType: 'json',
            data: {
                'options_name': $('#select-options').val()
            },
            success: function(response){
                $('#options-name').val(response.option_name);
                $('#options-name').attr('title', response._id);
                $('#keyword').val(response.keyword);
                $('#download-delay').val(response.delay);
                $('#begin-page-num').val(response.begin_page);
                $('#end-page-num').val(response.end_page);
                $('#_T_WM').val(response.cookies_T_WM);
                $('#SUHB').val(response.cookies_SUHB);
                $('#SUB').val(response.cookies_SUB);
                $('#gsid_CTandWM').val(response.cookies_gsid_CTandWM);
            }
        });
    });

    $('#edit-option').on('click', function(){
        $('.option').each(function(){
            $(this).attr('disabled', false);
        });
        $('#submit-option').css('display', 'none');
        $('#save-option').css('display', 'block');
        $('#cancel').css('display', 'block');
    });

    $('#cancel').on('click', function(){
        $('.option').each(function(){
            $(this).attr('disabled', true);
        });
        $('#save-option').css('display', 'none');
        $('#submit-option').css('display', 'none');
        $('#cancel').css('display', 'none');
    });

    $('#save-option').on('click', function(){
        var _id = $('#options-name').attr('title'),
            optionsName = $('#options-name').val(),
            keyword = $('#keyword').val(),
            delay = $('#download-delay').val(),
            beginPage = $('#begin-page-num').val(),
            endPage = $('#end-page-num').val(),
            t_wm = $('#_T_WM').val(),
            suhb = $('#SUHB').val(),
            sub = $('#SUB').val(),
            gsid_CTandWM = $('#gsid_CTandWM').val(),
            user_id = $("#user").attr('index');

        $.ajax({
            url: '/save/',
            type: 'POST',
            data: {
                '_id': _id,
                'optionsName': optionsName,
                'keyword': keyword,
                'delay': delay,
                'beginPage': beginPage,
                'endPage': endPage,
                't_wm': t_wm,
                'suhb': suhb,
                'sub': sub,
                'gsid_CTandWM': gsid_CTandWM,
                'user_id': user_id
            },
            success: function(response){
                if( response === 'True' ){
                    $('#msg').html('');
                    $('#msg').append('<p>Save Success!</p>');
                    $('#msg-modal').modal('show');
                }else{
                    $('#msg').html('');
                    $('#msg').append('<p>Save Fail!</p>');
                    $('#msg-modal').modal('show');
                }
                $('.option').each(function(){
                    $(this).attr('disabled', true);
                });
                $('#save-option').css('display', 'none');
                $('#cancel').css('display', 'none');
            }
        });
    });

    function Push(){
        var timer = null;

        timer = setInterval(function(){
            $.ajax({
                url: '/process_status/',
                type: 'POST',
                success: function(response){
                    console.log(response);
                    if( parseInt(response) === 0 || response !== 'None'){
                        $('.status-msg').html('<div class=\'running-tips font-red\'>Spider is stoped!</div>');
                        $('.stop-btn-box').hide();
                        clearInterval(timer);
                    }
                }
            });
        }, 3000);
    }

    $('#begin-crawl').on('click', function(){
        var _id = $('#options-name').attr('title');

        $.ajax({
            url: '/crawl/',
            type: 'POST',
            data: {
                '_id': _id,
            },
            success: function(response){
                $('#crawl-status-box').show();
                $('.status-msg').show();
                $('.status-msg').html('<div class=\'success-circle\'></div><div class=\'running-tips\'>Spider is running...</div>');
                $('.stop-btn-box').show();
                if (response === 'None'){
                    Push();
                }else{
                    $('.status-msg').html('<div class=\'running-tips font-red\'>Spider is stoped!</div>');
                    $('.stop-btn-box').hide();
                }
            }
        });
    });

    $('#stop-crawl').on('click', function(){
        $.ajax({
            url: '/stop_crawl/',
            type: 'POST',
            success: function(response){
                $('.status-msg').html('<div class=\'running-tips font-red\'>Spider is stoped!</div>');
                $('.stop-btn-box').hide();
            }
        });
    });
}());