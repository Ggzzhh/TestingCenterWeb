function MyMessage(user_id, message) {
    var json_data = JSON.stringify({'user_id': user_id, 'message': message});
    $.ajax({
        type: "POST",
        url: "/api-v1.0/message",
        data: json_data,
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            if (data.result !== 'ok'){
                swal('错误','发送失败！请联系管理人员！', 'error')
            }
            else{
                console.log('发送成功')
            }
        },
        error: function () {
            swal('错误','发送失败！请联系管理人员！', 'error')
        }
    })
}