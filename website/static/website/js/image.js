$(document).ready(function(){
  	$('.image-space').addClass('active');

    $('.image-create ul li').click(function() {
        $('.image-create ul li').removeClass('active');
        $(this).addClass('active');
        $('.image-create .tab-pane').removeClass('in');
        $('.image-create .tab-pane').removeClass('active');
        var id = $(this).children('a')[0].getAttribute('data-id');
        $('#' + id).addClass('in');
        $('#' + id).addClass('active');
    });

    $('.image-create .fileupload').fileupload({
        dataType: 'json',

        add: function (e, data) {
            $('.progress').css('display', 'block');
            data.submit();
        },

        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100 - 1);
            $('.progress .progress-bar').css(
                'width',
                progress + '%'
            );
            $('.progress .progress-bar').text(progress + '%');
        },

        done: function(e, data) {
            $('.progress .progress-bar').css('width', '100%');
            $('.progress .progress-bar').text("finished");
            $('.progress').removeClass('active');
        }
    });

    $('.image-create .submit').click(function() {
        $('.image-create .submit').val("上传中...");
        var form = $(this).parents("form");
        var url = window.location.href.split("#")[0];
        var create_url = url.replace("images", "create-image");
        var data = form.serialize();

        $.ajax({
            cache: true,
            type: "POST",
            url: create_url,
            data: data,
            async: false,
            success: function(data) {
                if (data.hasOwnProperty("success")) {
                    form[0].reset();
                    window.location.href = url;
                }
                else {
                    $('.image-create .submit').val(" 上 传 ");
                    $('.image-create .submit-notice').html("上传失败！");
                }
            },
            error: function(request) {
                $('.image-create .submit').val(" 上 传 ");
                $('.image-create .submit-notice').html("上传失败！");
            }
        });
    });

    $('.app-create .submit').click(function() {
        $('.app-create .submit').val("创建中...");
        var form = $(this).parents("form");
        var url = window.location.href.split("images")[0];
        var application_url = url + "applications/";
        var create_url = url + "create-application/";
        var data = form.serialize();

        $.ajax({
            cache: true,
            type: "POST",
            url: create_url,
            data: data,
            async: false,
            success: function(data) {
                if (data.hasOwnProperty("success")) {
                    form[0].reset();
                    window.location.href = application_url;
                }
                else {
                    $('.app-create .submit').val(" 创　建 ");
                    $('.app-create .submit-notice').html("创建失败！");
                }
            },
            error: function(request) {
                $('.app-create .submit').val(" 创　建 ");
                $('.app-create .submit-notice').html("服务器出错！");
            }
        });
    });

    $('#env-add').click(function() {
        var number = parseInt($('#env-number').val());
        var row = get_env_row(number);
        $('#env-table').append(row);
        $('#env-number').val(number + 1);
    });

    $('#env-del').click(function() {
        var number = parseInt($('#env-number').val()) - 1;
        if (number == -1)
            return;
        $('#env_' + number).remove();
        $('#env-number').val(number);
    });

    $('#port-add').click(function() {
        var number = parseInt($('#port-number').val());
        var row = get_port_row(number);
        $('#port-table').append(row);
        $('#port-number').val(number + 1);
    });

    $('#port-del').click(function() {
        var number = parseInt($('#port-number').val()) - 1;
        if (number == -1)
            return;
        $('#port_' + number).remove();
        $('#port-number').val(number);
    });

    $('#volume-add').click(function() {
        var number = parseInt($('#volume-number').val());
        var row = get_volume_row(number);
        $('#volume-table').append(row);
        $('#volume-number').val(number + 1);
    });

    $('#volume-del').click(function() {
        var number = parseInt($('#volume-number').val()) - 1;
        if (number == -1)
            return;
        $('#volume_' + number).remove();
        $('#volume-number').val(number);
    });

    $('#scale #autoscaler').change(function() {
        var val = $('#scale #autoscaler').val();
        if (val == 'false') {
            $('#scale .config').remove();
        }
        else {
            $('#scale').append(get_scale_config());
        }
    });
});

function show_image(element) {
    var id = $(element).find("input").first().val();
    var base_url = window.location.href.split("#")[0];
    var new_url = base_url + id + "/";
    window.location.href = new_url;
}

function get_env_row(number) {
    var name = "env_name_" + number;
    var value = "env_value_" + number;
    var id = "env_" + number;
    return '<tr id="' + id + '">\
                <td  class="col-sm-1">\
                    <input type="text" class="form-control" name="' + name + '" placeholder="键">\
                </td>\
                <td class="col-sm-1">\
                    <input type="text" class="form-control" name="' + value + '" placeholder="值">\
                </td>\
                </tr>';
}

function get_port_row(number) {
    var name = "port_name_" + number;
    var value = "port_value_" + number;
    var protocol = "port_protocol_" + number;
    var id = "port_" + number;
    return '<tr id="' + id + '">\
                    <td  class="col-sm-1">\
                        <input type="text" class="form-control" name="' + name + '" placeholder="端口名">\
                    </td>\
                    <td class="col-sm-1">\
                        <input type="text" class="form-control" name="' + value + '" placeholder="端口号">\
                    </td>\
                    <td class="col-sm-1">\
                        <select class="form-control" name="' + protocol + '">\
                            <option value="TCP">TCP</option>\
                            <option value="UDP">UDP</option>\
                        </select>\
                    </td>\
                </tr>';
}

function get_volume_row(number) {
    var obj = eval("(" + $('#volumes').val() + ")");
    var options = "";
    for (var i = 0; i < obj.length; i++) {
        options += '<option value="' + obj[i].id + '">' + obj[i].name + '</option>';
    }

    var name = "volume_name_" + number;
    var path = "volume_path_" + number;
    var id = "volume_" + number;
    return '<tr id="' + id + '">\
                <td class="col-sm-1">\
                    <select class="form-control" name="' + name + '">\
                        ' + options + '\
                    </select>\
                </td>\
                <td  class="col-sm-1">\
                    <input type="text" class="form-control" name="' + path + '"\ placeholder="挂载目录">\
                </td>\
                </tr>';
}

function get_scale_config() {
    return '<div class="config form-group">\
            <label class="col-sm-2 control-label">扩容配置</label>\
            <div  class="col-sm-2">\
                <input type="text" class="form-control" name="min_replicas"\ placeholder="最小副本数">\
            </div>\
            <div class="col-sm-3">\
                <input type="text" class="form-control" name="max_replicas"\ placeholder="最大副本数(-1为无限制)">\
            </div>\
            <div class="col-sm-3">\
                <input type="text" class="form-control" name="cpu_target"\ placeholder="CPU阈值百分数(1~100)">\
            </div>\
        </div>';
}
