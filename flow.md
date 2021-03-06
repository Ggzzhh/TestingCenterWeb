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
        
6. 后台数据库
    * 会员
        * id
        * 邮箱
        * 密码hash
        * 真实姓名
        * 昵称
        * 年龄
        * 性别
        * 身高
        * 体重
        * 位置
        * qq
        * 微信
        * 手机号（账号）
        * 发布的文章
        * 发布的评论
        * 所属队伍/自由球员
        * 是否队长
        * 是否协管
    * 队伍数据库
        * id
        * 队伍名
        * 队长
        * 申请者
        * 队员
    * 申请入队数据库
        * id
        * 申请人id
        * 队伍id
    * 咨询类别
        * id
        * 咨询类别
    * 咨询数据库
        * id
        * 发布时间
        * 发布方
        * 所属类别id
        * 评论
    * 评论数据库
        * id
        * 文章id
        * 发布者id
        * 评论内容
        * 评论时间
    * 单人活动管理
        * 报名时间
        * 活动id
        * 报名人id
    * 多人活动管理
        * 报名时间
        * 活动id
        * 报名团队id
    * 赛事
        * id
        * 参赛队伍1
        * 参赛队伍2
        * 参赛队伍1分数
        * 参赛队伍2分数
        * 获胜队伍
        * 比赛时间
    * 活动
        * id
        * 活动名
        * 活动内容
    * 设置需求：
        * 关于我们
        * 公司名称
        * 地址
        * 联系人
        * 联系方式
        * 微信
        * 微博
        * 文章二级页（单独表）
        * 协管列表（通过账号查询添加, 不列入数据库）
7. 使用wangEditor编辑器
8. 部分使用瀑布式布局
9. 设计实现首页
10. 完成注册以及验证功能
11. 登录以及邮箱验证
12. 活动页面以及报名页面  分成单人/多人两个表格即可

* 部署腾讯云
    * 在腾讯云的CentOS部署
    * 1.准备python环境
         sudo yum install gcc-c++
         安装python3.6 按照https://www.cnblogs.com/cloud-80808174-sea/p/6902934.html
         配置pip3 ln -s /usr/python3.6/bin/pip3 /usr/bin/pip3
    * 2.配置flask环境
         pip freeze | tee requirements.txt # 输出本地包环境至文件
         pip install -r requirements.txt # 根据文件进行包安装    