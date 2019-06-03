
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


     table = $('#devicedatables').DataTable({
        "processing":true ,
        // "serverSide": true,
        "ajax": {
            "url": "/dashboard/api/devicelist/",
            "type": "GET"
        },
        "columns":[
            // {"data":"id"},
            {"data":"device_name"},
            {"data":"device_id"},
            {"data":"access_token"},
            {"data":"device_check",
             "render":function (data,type,row) {
                 return (data === 1) ? '<span class="glyphicon glyphicon-ok">' +
                     '</span>' : '<span class="glyphicon glyphicon-remove"></span>';
             }
                },
            // {"data":"path_to_coupon_image_url_link"},
            // {"data":"coupon_image_url_link",
            //  "render": function(data, type, row) {
            //     return '<img src="'+data+'" style="height:100px;width:200px;"/>';}
            // },

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
     deviceCheck='';
     $('#devicedatables tbody').on('click', '.btn-dark', function (){
        data = table.row($(this).parents('tr')).data();
        $("#device_id").val(data['device_id']);
        $("#device_name").val(data['device_name']);
        $("#access_token").val(data['access_token']);
        if(data['device_check']===1){
            $('#deviceCheck').addClass('glyphicon glyphicon-ok');
        }else {
            $('#deviceCheck').addClass('glyphicon glyphicon-remove');
        }
        deviceCheck=data['device_check'];
        $("#deviceEditModal").modal();
        ID=data['id'];
    });



    $('#devicedatables tbody').on('click', '.btn-danger', function (){
        data = table.row($(this).parents('tr')).data();
        ID=data['id'];
        $("#deviceDeleteModal").modal();
    });

    $('#deviceFormEdit').on('submit',function (event ) {
        event.preventDefault();
        // $this=
        url='/dashboard/api/devicelist/';
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

    $('#deviceDeleteModal').on('click', '#delete', function (e) {

        url='/dashboard/api/devicelist/';
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

    $('#newDevice').on('click',function (e) {
        $("#deviceNewModal").modal();

    });

    $('#deviceFormNew').on('submit',function (event ) {
        event.preventDefault();
        // $this=
        url='/dashboard/api/devicelist/';
        method='POST';
        // urlAPI=url+ID+'/';

    $.ajax({
        url:url,
        method:method,
        data: $(this).serialize(),
        success:function (data) {
                    location.reload();
            }
        });
    });
});
