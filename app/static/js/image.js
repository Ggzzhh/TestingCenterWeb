function Upload(img, url) {
    // 用ajax上传图片或者文件
    var data = new FormData();
    data.append('File', img);
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: 'json',
        contentType: false
    })
        .done(function(data) {    //上传成功
            if(data.status == true){
                console.log("success");
                return data.data
            }
        })
        .fail(function() {
            console.log("GG,failed");
        })
        .always(function() {
            console.log("complete");
        });
}

// 参数 img 是需要上传压缩的图片
// 参数Preview_id 是预览的img标签的id
// 默认: 宽度以及高度为140
function upLoadImage(img, Preview_id) {
    var reader = new FileReader();

    reader.readAsDataURL(img);
    // console.log(img.length);

    reader.onerror = function () {
        console.log("读取异常....");
    };

    reader.onload = function () {
        // 压缩 经测试 确实会变小
        // 创建canvas元素
        var canvas = document.createElement("canvas");
        // 创建2d画布 getContext() 方法返回一个用于在画布上绘图的环境。
        var ctx = canvas.getContext('2d');
        var image = new Image();
        image.src = this.result;
        return image.onload = function () {
            // 注释内是等比例缩放
            var width = 140; // image.width;
            var height = 140; // image.height;
            // var old_width = image.width;
            // var old_height = image.height;
            // if (old_width > 200 && old_width >= old_height) {
            //     width = 200;
            //     height = (200 * old_height) / old_width;
            // }
            // if (old_height > 200 && old_width >= old_height ) {
            //     height = 200;
            //     width = (200 * old_width) / old_height;
            // }
            canvas.width = width;
            canvas.height = height;

            ctx.drawImage(image, 0, 0, width, height);
            var newImage = canvas.toDataURL("image/jpeg", 0.7);
            // console.log(newImage);
            $('#'+ Preview_id).attr("src", newImage);
            // document.getElementById('uploadPreview').src =
        };
    };
}