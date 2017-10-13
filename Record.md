#开发过程中遇到的需要注意的事情

## 数据库
* SQLALCHEMY_RECORD_QUERIES告诉Flask-SQLAlchemy启用记录查询统计数字的功能，
缓慢查询的阈值设为0.5秒，这两个配置变量都在Config基类中设置，因此在所有环境中都可使用
* 每当发现缓慢查询，Flask程序的日志记录器就会写入一条记录，若想保存这些日志记录，
必须配置日志记录器，日志记录器的配置根据程序所在主机使用的平台而有所不同。

## PyCharm新建Flask项目无法关联jinja2的问题
    设置Python>Template>Lanuages
    
## 关于Flask_login
    * 出现错误:<br>
         `No user_loader has been installed for this LoginManager. 
         Add one with the 'LoginManager.user_loader' decorator.`
     原因是:
         flask要求用户实现一个回调函数 返回用户对象或者None
         在model文件中实现
 
## Flask 让jsonify返回的json串支持中文显示
    设置 app.config['JSON_AS_ASCII'] = False
参考资料：
>http://blog.csdn.net/fo11ower/article/details/70062524

## CSS 中height以及width 100%无效的问题
    height:100% 必须从html开始一级一级顺延下来
    width 则不用
    
## 每次变更js或者css文件后,需要清空记录后重新加载方可生效
    目前chrome中是这样
    
## 在用jquery的事件时, 调用外部文件的方法
    在事件的莫名函数内部调用
 ```javascript
 $("#uploadImage").change(function () {
    upLoadImage(this.files[0], 'uploadPreview');
 });
 ```
 
## Js 操作json
    JSON.parse()	用于将一个 JSON 字符串转换为 JavaScript 对象。
    JSON.stringify()	用于将 JavaScript 值转换为 JSON 字符串。
    
## 导航变色关键
```javascript
<script>
    $(window).scroll(function () {
        // scroll 目标发生滚动事件
        // 如果.navbar 的距离top的偏移量大于50 添加类
        if ($(".navbar").offset().top > 50) {
            $(".navbar-fixed-top").addClass("top-nav");
        }else {
            $(".navbar-fixed-top").removeClass("top-nav");}
    })
</script>
```

## 使用pagedown来修饰markdown富文本

    给app注册pagedown类
    使用页面插入  `{{ pagedown.include_pagedown() }}`
    在modles的模型中处理markdown文本 因为
    
## 使用flask_wtf 进行 CSRF 保护
参考:
><http://flask-wtf.readthedocs.io/en/stable/csrf.html?highlight=csrf>

## 使用编辑器上传多个图片
    传入的数据类型是
>设置文件名`editor.customConfig.uploadFileName = 'File';`<br/>
获取多个图片`files = request.files.getlist("File")`
<br>参考flask官方文档

## 数据库迁移报错 not up date
    删除表重新执行一遍 bd init    db migrate    db.create_all()

## js中的FormDate对象发送至api
    需要设置 ： processData:false, contentType: false,
    
## 瀑布流布局使用js插件--masonry
    初次加载
    $('#容器id').masonry()
    刷新
    $('#容器id').masonry('reloadItems').masonry();
cdn地址: <https://cdn.bootcss.com/masonry/4.2.0/masonry.pkgd.js>
    
## 无限制下拉刷新 jquery
```javascript
    // 滚动条到页面底部加载更多案例
        // scroll方法用来监听滚动事件
        $(window).scroll(function(){
            var scrollTop = $(this).scrollTop();    //滚动条距离顶部的高度
            var scrollHeight = $(document).height();   //当前页面的总高度
            var clientHeight = $(this).height();    //当前可视的页面高度

            if(scrollTop + clientHeight >= scrollHeight - 10){
                // console.log('当滚动条距离底部10的时候');
                if (next !== null && next > 1){
                    // 添加内容
                    get_page(next);
                    next = null;
                }
            }
            // else if(scrollTop<=0){
                // console.log('滑动到顶部')
            // }
        });
```

## 借用moment.js使时间格式化
```javascript
// moment设定语言
moment.locale('zh-cn');
// 两种时间表示
moment(content).format("YYYY年MMMD H:mm:ss" );  // 2017年10月12 15:09:22
moment(content).fromNow();  // 21分钟前
```
>官方文档<http://momentjs.com/>