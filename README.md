README
==================

## 网站建设主旨
    通过建设一个RESTful风格的网站来达到练习flask以及前端页面的目的
    建设一个功能完善的检测中心网站 最好避免维护


## 项目结构
    * 初步设定，后期继续增加
    |-TestingCenterWeb
        |-app/                  网站应用
            |-templates/        静态模板
            |-static/           静态文件 css/js
            |-main/             网站主体部分 REST风格设计
                |-__init__.py   主体部分初始化
                |-errors.py     错误处理
                |-forms.py      表单处理
                |-views.py      视图处理
            |-__init__.py       网站初始化
            |-email.py          邮箱相关操作
            |-models.py         模板相关
            |-decorators.py     装饰器
        |-migrations/           数据库迁移使用
        |-tests/                自动化测试处理
            |-__init__.py       测试初始化
            |-test*.py          测试程序
        |-venv/                 版本控制
        |-requirements.txt      所有依赖包
        |-config.py             存储配置
        [test]: |-manage.py             用于启动程序以及其他的程序任务


## 角色设定

    1. 超级管理员 负责给予权限 以及拥有所有权限
    2. 网站管理员 可以给网站添加文章 修改内容等
    3. 匿名用户   拥有查询证书状态以及浏览的权限


## 后台编辑器

    使用百度免费的UEditor富文本编辑器
    地址:[<https://github.com/fex-team/ueditor>](https://github.com/fex-team/ueditor "官方github")

