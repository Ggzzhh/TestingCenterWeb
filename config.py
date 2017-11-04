# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基础配置，导入所有配置中"""
    # 密匙
    SECRET_KEY = os.environ.get('SECRET_KEY') or "PDSHHTY"

    # 数据库自动提交数据
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
    # 这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询耗时过长的时间
    SLOW_DB_QUERY_TIME = 0.5

    # 可以用于显式地禁用或者启用查询记录
    SQLALCHEMY_RECORD_QUERIES = True

    # 邮件主题前缀
    MAIL_SUBJECT_PREFIX = '<平顶山浩瀚体育>'

    # 寄件人名称
    MAIL_SENDER = '平顶山浩瀚体育 <gggzh@139.com>'

    # 邮箱端口号
    MAIL_PORT = 465

    # 139邮箱smtp服务器地址
    MAIL_SERVER = 'smtp.139.com'

    # 发送邮件时使用TLS安全协议 默认为False
    MAIL_USE_TLS = False

    # 发送邮件时使用SSL安全协议 默认为False
    MAIL_USE_SSL = True

    # 发送邮件所用的邮箱用户名以及密码
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # 管理员邮箱
    ADMIN_MAIL = os.environ.get('ADMIN_EMAIL')
    # 管理员账号
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    # 管理员密码
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin'
    # SSL安全协议开关 False会打开
    SSL_DISABLE = True

    # 禁止转换asc码
    JSON_AS_ASCII = False

    # 存储图片的位置
    UPLOAD_FOLDER = 'app\static\image'

    # 分页设置
    POSTS_PER_PAGE = 15

    # 配置类可以定义 init_app() 类方法，其参数是程序实例。
    # 在这个方法中，可以执行对当前 环境的配置初始化。
    # 现在，基类 Config 中的 init_app() 方法为空。
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """开发配置 以及开发时使用的数据库地址"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    """测试配置 以及测试时使用的数据库地址"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    """正常使用时的配置 以及数据库地址 发生错误时自动发送邮件"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
         'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 发生错误时自动发送错误日志到管理员邮箱
        import logging
        from logging.handlers import SMTPHandler

        credentials = None  # 凭证
        secure = None  # 安全保护

        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        # 邮件处理设置
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.ADMIN_MAIL],
            subject=cls.MAIL_SUBJECT_PREFIX + "网站发生错误",
            credentials=credentials,
            secure=secure)
        # 设置此处理程序的日志级别
        mail_handler.setLevel(logging.ERROR)
        # 给app添加错误处理程序
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}





