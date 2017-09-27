# 第一次流程

1. 配置config
    * 通过 `basedir = os.path.abspath(os.path.dirname(__file__))` 获取app所在地址
    * 创建基础设置类Config,一般包括：
        * 密匙、数据库配置、管理员信息、分页数、邮箱配置等 
    
2. 初始化所有应用程序app\\\_\_init__.py
    * 导入依赖包，在工厂函数内初始化app
    * 在app下个大文件夹内的__init__文件中构造蓝图，并在此进行蓝图注册
    
3. 设置manage.py 管理整个app

4. 注意Flask-Login要求实现的用户方法，否则会报错，如果不使用，暂时不要注册。
   FlaskLogin 提供了一个 UserMixin 类

5. 制作网站后台页面
    * 实现登录功能
    * 加密使用：
        * Flask-Login：管理已登录用户的用户会话。
        * Werkzeug：计算密码散列值并进行核对。
        * itsdangerous：生成并核对加密安全令牌