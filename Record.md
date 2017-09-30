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