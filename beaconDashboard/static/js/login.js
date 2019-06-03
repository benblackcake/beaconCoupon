

$(document).ready(function() {
     function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $('#formlogin').on('submit',function (event ) {
        event.preventDefault();
        // $this=
        url='/dashboard/testlogin';
        method='POST';
        // urlAPI=url+ID+'/';

        $.ajax({
            url:url,
            method:method,
            data: $(this).serialize(),
            success:function (data) {
                if(data=='success')
                    location.reload();
                else
                    alert("帳號密碼錯誤")
                }
            });
    });

    $('#formregist').on('submit',function (event) {
        event.preventDefault();
        url='/dashboard/api/staffregist/';
        method='POST';

        $.ajax({
            url:url,
            method:method,
            data: $(this).serialize(),

            success:function (data) {
                if (data=='success')
                    location.reload('dashboard/');
                else
                alert("帳號已有人申請")
                }

        });

    })
});
