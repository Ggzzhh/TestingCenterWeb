# 第一次流程

1. 配置config
    * 通过 `basedir = os.path.abspath(os.path.dirname(__file__))` 获取app所在地址
    * 创建基础设置类Config,一般包括：
        * 密匙、数据库配置、管理员信息、分页数、邮箱配置等 
    
2. 初始化所有应用程序app\\\_\_init__.py
    * 导入依赖包，在工厂函数内初始化app
    * 在app下个大文件夹内的__init__文件中构造蓝图，并在此进行蓝图注册