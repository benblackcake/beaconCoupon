
//
//var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
//

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


     table = $('#datatables').DataTable({
        "processing":true ,
        // "serverSide": true,
        "ajax": {
            "url": "/dashboard/api/userlist/",
            "type": "GET"
        },
        "columns":[
            // {"data":"id"},
            {"data":"coupon_name"},
            {"data":"coupon_content"},
            {"data":"coupon_dismoney"},
            {"data":"coupon_s_time"},
            {"data":"coupon_e_time"},
            {"data":"path_to_coupon_image_url_link"},
            {"data":"coupon_image_url_link",
             "render": function(data, type, row) {
                return '<img src="'+data+'" style="height:100px;width:200px;"/>';}
            },

            // {"data":"coupon_id"},
            {
                "data": null,
                "defaultContent": '<button type="button" class="btn btn-dark">Edit</button>'
                + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-danger">Delete</button>'
            }
        ]

    });
     ID="";
     $('#datatables tbody').on('click', '.btn-dark', function (){
        data = table.row($(this).parents('tr')).data();
        $("#coupon_name").val(data['coupon_name']);
        $("#coupon_content").val(data['coupon_content']);
        $("#coupon_dismoney").val(data['coupon_dismoney']);
        $("#coupon_s_time").val(data['coupon_s_time']);
        $("#coupon_e_time").val(data['coupon_e_time']);
        $("#myModal").modal();
        ID=data['id'];
    });

    $('#datatables tbody').on('click', '.btn-danger', function (){
        data = table.row($(this).parents('tr')).data();
        ID=data['id'];
        $("#confirmDelete").modal();
    });

    $('#formEdit').on('submit',function (event ) {
        event.preventDefault();
        // $this=
        url='/dashboard/api/userlist/';
        method='PUT';
        urlAPI=url+ID+'/';

    $.ajax({
        url:urlAPI,
        method:method,
        data: $(this).serialize(),
        success:function (data) {
                    location.reload();
            }
        });
    });

    $('#confirmDelete').on('click', '#delete', function (e) {

        url='/dashboard/api/userlist/';
        method='DELETE';

        urlAPI=url+ID+'/';
        $.ajax({
            url:urlAPI,
            method: method,
                success:function (data) {
                location.reload();
            }
        });
    });
});
