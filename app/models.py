# -*- coding: utf-8 -*-
import hashlib
from random import randint
from datetime import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach


@login_manager.user_loader
def load_user(user_id):
    """使用flask_login时必须实现的函数 返回None或者实例"""
    return Administrator.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    """匿名用户类"""
    def can(self):
        return False

    def is_administrator(self):
        return False

    def get_names(self):
        return []

login_manager.anonymous_user = AnonymousUser


class Administrator(UserMixin, db.Model):
    """管理员表 整个网站只设置一个管理员账号, 需要在命令行手动注册"""

    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("这不是一个可读属性")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码，返回布尔值"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register_admin():
        """注册管理员账号"""
        db.create_all()
        only_admin = Administrator(username=current_app.config['ADMIN_USERNAME'])
        only_admin.password = current_app.config['ADMIN_PASSWORD']
        db.session.add(only_admin)
        db.session.commit()

    def get_names(self):
        names = []
        for name in SecondPageName.query.all():
            names.append((name.page_name, name.url))
        return names


class WebSetting(db.Model):
    """网站设置"""
    __tablename__ = 'web_settings'
    id = db.Column(db.Integer, primary_key=True)
    corporate_name = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    address = db.Column(db.String(128))
    phone_num = db.Column(db.Integer)
    WeChat = db.Column(db.String(32))
    WeChat_img = db.Column(db.Text)
    sina_blog = db.Column(db.String(64))
    email = db.Column(db.String(32))
    contacts = db.Column(db.String(32))
    qq = db.Column(db.String(32))
    about_me_html = db.Column(db.Text)

    def to_json(self):
        """把网站设置转换为字典 返回出去"""
        json_web_setting = {
            'corporate_name': self.corporate_name,
            'about_me': self.about_me,
            'address': self.address,
            'phone_num': self.phone_num,
            'WeChat': self.WeChat,
            'WeChat_img': self.WeChat_img,
            'sina_blog': self.sina_blog,
            'email': self.email,
            'contacts': self.contacts,
            'qq': self.qq
        }
        return json_web_setting

    def from_json(self, json_data):
        """通过json数据更新网站设置"""
        setting = WebSetting.query.first()
        if setting is None:
            return WebSetting(
                corporate_name=json_data.get('corporate_name'),
                about_me=json_data.get('about_me'),
                address=json_data.get('address'),
                phone_num=json_data.get('phone_num'),
                WeChat=json_data.get('WeChat'),
                WeChat_img=json_data.get('WeChat_img'),
                sina_blog=json_data.get('sina_blog'),
                email=json_data.get('email'),
                contacts=json_data.get('contacts'),
                qq=json_data.get('qq')
            )
        self.corporate_name = json_data.get('corporate_name')
        self.about_me = json_data.get('about_me')
        self.address = json_data.get('address')
        self.phone_num = json_data.get('phone_num')
        self.WeChat = json_data.get('WeChat')
        self.WeChat_img = json_data.get('WeChat_img')
        self.sina_blog = json_data.get('sina_blog')
        self.email = json_data.get('email')
        self.contacts = json_data.get('contacts')
        self.qq = json_data.get('qq')
        return self

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        set事件的监听程序，只要about_me设置新值，该函数自动被调用
        主要作用是把body字段中的文本渲染成HTML格式，结果在保存在body_html中
        """
        # 允许使用的html标签
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        # 转换过程
        # 1.markdown将文本转换成html
        # 2.bleach.clean 清除掉不符合白名单的标签
        # 3.bleach.linkify 转换文本中类似url以及邮箱为a连接
        target.about_me_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

# 监听set事件 只要body设置了新值，就会调用on_changed_body
db.event.listen(WebSetting.about_me, 'set', WebSetting.on_changed_body)


class SecondPageName(db.Model):
    """发布文章二级页面名称管理表"""
    __tablename__ = 'nav_settings'
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(32))
    url = db.Column(db.String(64))
    posts = db.relationship('Post', backref='category', lazy='dynamic',
                            cascade='all, delete-orphan')

    def to_json(self):
        names = SecondPageName.query.all()
        json_data = {}
        lacks = []
        if not names:
            lacks = [1, 2, 3]
            json_data = {
                'num': 0,
                'lacks': lacks
            }
        else:
            for num in range(1, 4):
                if SecondPageName.query.get(num) is None:
                    lacks.append(num)
            json_data = {
                'num': len(names),
                'lacks': lacks,
                'names': [(name.id, name.page_name) for name in names],
            }
        return json_data

    def from_json(self, json_data):
        if json_data is None:
            return None
        name_1 = json_data.get('1')
        name_2 = json_data.get('2')
        name_3 = json_data.get('3')
        names = []
        if name_1:
            pagename1 = SecondPageName.query.filter_by(id=1).first()
            if pagename1 is None:
                pagename1 = SecondPageName(id=1)
            pagename1.page_name = name_1
            pagename1.url = url_for('manage.posts', category_id=1)
            names.append(pagename1)
        if name_2:
            pagename2 = SecondPageName.query.filter_by(id=2).first()
            if pagename2 is None:
                pagename2 = SecondPageName(id=2)
            pagename2.page_name = name_2
            pagename2.url = url_for('manage.posts', category_id=2)
            names.append(pagename2)
        if name_3:
            pagename3 = SecondPageName.query.filter_by(id=3).first()
            if pagename3 is None:
                pagename3 = SecondPageName(id=3)
            pagename3.page_name = name_3
            pagename3.url = url_for('manage.posts', category_id=3)
            names.append(pagename3)
        if len(SecondPageName.query.all()) > 3:
            names = None
        return names


class Post(db.Model):
    """发布文章模版"""
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    image_url = db.Column(
        db.String(64), default='/static/image/default.jpg')
    abstract = db.Column(db.String(200))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey('nav_settings.id'))

    def to_json(self):
        json_post = {
            'id': self.id,
            'title': self.title,
            'edit_url': url_for('manage.get_post', id=self.id, _external=True),
            'image_url': self.image_url,
            'body_html': self.body_html,
            'abstract': self.abstract,
            'timestamp': self.timestamp  # ,
            # 'category': [self.category.page_name, url_for(
            #     'manage.posts', category_id=self.category_id)]
        }
        return json_post

    @staticmethod
    def from_json(json_data):
        """从前台传来的json数据中创建新文章"""
        id = json_data.get('id')
        body_html = json_data.get('body_html')
        title = json_data.get('title')
        image_url = json_data.get('image_url')
        abstract = json_data.get('abstract')
        if title is None or title == '':
            raise ValueError('文章不能为空或json数据错误')
        if id is not None:
            post = Post.query.get_or_404(id)
            post.title = title
            post.body_html = body_html
            post.abstract = abstract
            post.image_url = image_url
            return post
        return Post(body_html=body_html, abstract=abstract,
                    title=title, image_url=image_url)

    @staticmethod
    def add_post(num=100):
        """添加100文章进行测试"""
        for i in range(num):
            post = Post(title="测试用文章"+str(i), abstract="我是来卖萌的" * randint(1,
                                                                          10),
                        image_url="/static/image/3.gif", body_html="卖萌可耻" * i)
            post.category_id = randint(1, 3)
            db.session.add(post)
        db.session.commit()


class Activity(db.Model):
    """活动模版"""
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), default='标题')
    img_url = db.Column(db.String(64))
    body = db.Column(db.Text)
    start_date = db.Column(db.DateTime, index=True)
    end_date = db.Column(db.DateTime, index=True)
    sign_up_url = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def to_json(self, brief=False):
        json_data = {
            'title': self.title,
            'api_url': url_for('api.get_activity', id=self.id),
            'edit_url': url_for('manage.edit_activity',
                                id=self.id, _external=True),
            'image_url': self.img_url,
            'body': self.body,
            'start_date': datetime.strftime(self.start_date, '%Y-%m-%d'),
            'end_date': datetime.strftime(self.end_date, '%Y-%m-%d'),
            'timestamp': self.timestamp
        }
        if brief:
            json_data.pop('body')
        return json_data

    @staticmethod
    def from_json(json_data):
        id = json_data.get('id')
        if id is not None:
            activity = Activity.query.get_or_404(id)
            activity.title = json_data.get('title')
            activity.img_url = json_data.get('img_url')
            activity.body = json_data.get('body')
            activity.start_date = datetime.strptime(json_data.get(
                            'start_date'), '%Y-%m-%d')
            activity.end_date = datetime.strptime(json_data.get(
                            'end_date'), '%Y-%m-%d')
            return activity
        return Activity(title=json_data.get('title'),
                        img_url=json_data.get('image_url'),
                        body=json_data.get('body'),
                        start_date=datetime.strptime(json_data.get(
                            'start_date'), '%Y-%m-%d'),
                        end_date=datetime.strptime(json_data.get(
                            'end_date'), '%Y-%m-%d'))


class FriendLink(db.Model):
    """友情链接模版"""
    __tablename__ = 'friend_links'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    url = db.Column(db.String(32))

    def to_json(self):
        json_data = {
            'name': self.name,
            'url': self.url
        }
        return json_data

    @staticmethod
    def from_json(data):
        return FriendLink(name=data.get('name'), url=data.get('url'))

    @staticmethod
    def update_from_json(data):
        id = data.get('id')
        if id is not None:
            link = FriendLink.query.get_or_404(id)
            link.name = data.get('name')
            link.url = data.get('url')
            return link
        return FriendLink.from_json(data)
