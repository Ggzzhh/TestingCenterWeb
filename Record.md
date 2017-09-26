#开发过程中遇到的需要注意的事情

## 数据库
* SQLALCHEMY_RECORD_QUERIES告诉Flask-SQLAlchemy启用记录查询统计数字的功能，
缓慢查询的阈值设为0.5秒，这两个配置变量都在Config基类中设置，因此在所有环境中都可使用
* 每当发现缓慢查询，Flask程序的日志记录器就会写入一条记录，若想保存这些日志记录，
必须配置日志记录器，日志记录器的配置根据程序所在主机使用的平台而有所不同。

## PyCharm新建Flask项目无法关联jinja2的问题
    设置Python Template Lanuages 即可