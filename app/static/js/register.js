function has_error(element, message) {
    $("#" + element).removeClass('has-success');
    $("#" + element).removeClass('has-error');
    $("#" + element).find('.help-block').html(message);
    $("#" + element).addClass('has-error')
}

function has_success(element) {
    $("#" + element).removeClass('has-success');
    $("#" + element).removeClass('has-error');
    $("#" + element).find('.help-block').html(
        "<span class='glyphicon glyphicon-ok' " +
        "aria-hidden='true'></span>");
    $("#" + element).addClass('has-success')
}

function register_re(re, val, element) {
    var error_message = {
        'username': '&times; 格式错误 请输入6至18位的字母、数字、下划线',
        'password': '&times; 格式错误 请输入6至18位的字母、数字、下划线',
        'email': '&times; 格式错误 请参照类似 \"假如我是QQ号@qq.com\" 的格式进行填写',
        'tops': '&times; 别闹 请填入正常的身高',
        'phone': '&times; 别闹 请填入正常的联通、移动、电信号',
        'weight': '&times; 别闹 请填入正常的体重',
        'age': '&times; 本网站只要10-99岁的',
        'qq': '&times; 别闹 哪有这样的QQ号'
    };

    if (re.test(val) === true){
        has_success(element);
        re_result[element] = true
    }
    else {
        has_error(element, error_message[element]);
        re_result[element] = false
    }
}

function repeat(element, re, val) {
    var data = {};
    var repeat_message = {
        'username': '&times; 该用户名已注册！',
        'email': '&times; 该邮箱已注册！',
    };
    data[element] = val;
    data = JSON.stringify(data);
    $.ajax({
        type: 'POST',
        url: "/api-v1.0/repeat",
        data: data,
        dataType: 'json',
        contentType: 'application/json;',
        success: function (data) {
            if (data.repeat === true) {
                has_error(element, repeat_message[element])
                re_result[element] = false
            }
            else{
                register_re(re, val, element);
                re_result[element] = true
            }
        }
    });
}

function bind_register() {
    // 监听input内容
    $('[name="username"]').bind( 'input propertychange change' ,function() {
        var re = /^[0-9a-zA-Z_]{6,18}$/;
        var val = $(this).val();
        repeat('username', re, val);
    });

    $('[name="email"]').bind( 'input propertychange change' ,function() {
        var re = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
        var val = $(this).val();
        repeat('email', re, val);
    });

    $('[name="password"]').bind( 'input propertychange change' ,function() {
        var re = /^[0-9a-zA-Z_]{6,18}$/;
        var val = $(this).val();
        register_re(re, val, 'password');
    });

    $('[name="phone"]').bind( 'input propertychange change' ,function() {
        var re = /^[1|9][0-9]{10}$/;
        var val = $(this).val();
        register_re(re, val, 'phone');
    });

    $('[name="qq"]').bind( 'input propertychange change' ,function() {
        var re = /^[1-9][0-9]{5,12}$/;
        var val = $(this).val();
        register_re(re, val, 'qq');
    });

    $('[name="age"]').bind( 'input propertychange change' ,function() {
        var re = /^[1-9][0-9]$/;
        var val = $(this).val();
        register_re(re, val, 'age');
    });

    $('[name="tops"]').bind( 'input propertychange change' ,function() {
        var re = /^[1-2][0-9]{2}$/;
        var val = $(this).val();
        register_re(re, val, 'tops');
    });

    $('[name="weight"]').bind( 'input propertychange change' ,function() {
        var re = /^[1-9][0-9]{1,2}$/;
        var val = $(this).val();
        register_re(re, val, 'weight');
    });
}