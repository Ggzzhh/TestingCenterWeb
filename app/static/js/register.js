function wrong(element) {
    var message = {
        'username': '&times; 格式错误 请输入不少于6位的字母、数字、下划线',
        'password': '&times; 格式错误 请输入不少于6位且不是纯数字的字母、数字、下划线',
        'email': '&times; 格式错误 请参照类似 \"假如我是QQ号@qq.com\" 的格式进行填写',
    };
    for (var i in message){
        if (i === element){
            $("#" + element + " .help-block").html(message[i]);
            $("#" + element).addClass('has-error')
        }
    }
}