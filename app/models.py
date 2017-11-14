# -*- coding: utf-8 -*-
import html
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
    if int(user_id) == 1:
        return Administrator.query.get(int(user_id))
    if int(user_id) >= 999:
        return User.query.get(int(user_id))
    return None


# 多对多关联表
# 单人报名表
solo = db.Table('solo',
                db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('activity_id',
                          db.Integer, db.ForeignKey('activities.id'))
                )

# 团队活动报名表
many = db.Table('many',
                db.Column('team_id', db.Integer, db.ForeignKey('teams.id')),
                db.Column('activity_id',
                          db.Integer, db.ForeignKey('activities.id'))
                )


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
    confirmed = db.Column(db.Boolean, default=True)

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

    @staticmethod
    def is_user():
        return False



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


class Comment(db.Model):
    """文章评论"""
    # todo: 搞定这里
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    body = db.Column(db.Text)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_json(self):
        """把评论转换成JSON格式的序列化字典"""
        json_comment = {
            # 'url': url_for('api.get_comment', id=self.id, _external=True),
            # 'post': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'timestamp': self.timestamp,
            # 'author': url_for('api.get_user', id=self.author_id, _external=True)
        }
        return json_comment


class Activity(db.Model):
    """活动模版"""
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), default='标题')
    img_url = db.Column(db.String(64))
    body = db.Column(db.Text)
    start_date = db.Column(db.DateTime, index=True)
    end_date = db.Column(db.DateTime, index=True)
    # 活动报名页面地址
    sign_up_url = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    # 报名关系
    is_solo = db.relationship('User', secondary=solo,
                              backref=db.backref('activities', lazy='dynamic'))
    is_team = db.relationship('Team', secondary=many,
                              backref=db.backref('activities', lazy='dynamic'))

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
            'timestamp': self.timestamp,
            'sign_up_url': self.sign_up_url
        }
        if brief:
            json_data.pop('body')
        return json_data

    def easy_to_json(self, brief=False):
        json_data = {
            'title': self.title,
            'image_url': self.img_url,
            'body': self.body,
            'start_date': datetime.strftime(self.start_date, '%Y-%m-%d'),
            'end_date': datetime.strftime(self.end_date, '%Y-%m-%d'),
            'timestamp': self.timestamp,
            'sign_up_url': self.sign_up_url,
            'show_url': url_for('main.activity', id=self.id),
        }
        if brief:
            json_data.pop('body')
        return json_data

    @staticmethod
    def from_json(json_data):
        id = json_data.get('id')
        if id is not None:
            activity = Activity.query.get_or_404(id)
        else:
            activity = Activity()
        activity.sign_up_url = json_data.get('select')
        activity.title = json_data.get('title')
        activity.img_url = json_data.get('image_url')
        activity.body = json_data.get('body')
        activity.start_date = datetime.strptime(json_data.get(
            'start_date'), '%Y-%m-%d')
        activity.end_date = datetime.strptime(json_data.get(
            'end_date'), '%Y-%m-%d')
        activity.number = json_data.get('number')
        return activity


class FriendLink(db.Model):
    """友情链接模版"""
    __tablename__ = 'friend_links'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    url = db.Column(db.String(32))

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }
        return json_data

    @staticmethod
    def from_json(data):
        return FriendLink(name=data.get('name'), url=data.get('url'))


class Carousel(db.Model):
    """首页轮播图"""
    __tablename__ = 'carousels'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(32), nullable=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'url': self.url
        }
        return json_data

    @staticmethod
    def from_json(data):
        return Carousel(url=data.get('url'))


class User(db.Model, UserMixin):
    """用户模版
        有一个默认的协助管理账户 id为999 这样用户注册时最小id即为1000
        管理者有权限删除留言
        删除留言后 在用户的通知信息中 显示信息
    """
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar()

    # 头像hash
    avatar_hash = db.Column(db.Text)

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    # 接收的信息
    infos = db.relationship("Info", backref='user', lazy='dynamic')
    # 必填
    username = db.Column(db.String(32), unique=True, nullable=True)
    email = db.Column(db.String(32), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    # 选填
    name = db.Column(db.String(16))
    phone = db.Column(db.Integer)
    # 昵称
    nickname = db.Column(db.String(32))
    # 1是男性 2女 3待定
    male = db.Column(db.Integer)
    age = db.Column(db.Integer)
    tops = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    position = db.Column(db.String(16))
    about_me = db.Column(db.Text)
    qq = db.Column(db.Integer)
    WeChat = db.Column(db.String(16))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    confirmed = db.Column(db.Boolean, default=False)

    @staticmethod
    def is_user():
        return False

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
    def is_position(value):
        """检验值是否是三个位置中的一个, 可删减"""
        positions = ['后卫', '前锋', '中锋']
        if value in positions:
            return True
        return False

    @staticmethod
    def default_user():
        """自动注册一个id为999的管理者， 之后注册的用户id从1000开始"""
        user = User(id=999, is_admin=True,
                    email=current_app.config['ADMIN_USERNAME'],
                    username='管理员')
        user.password = current_app.config['ADMIN_PASSWORD']
        db.session.add(user)
        db.session.commit()

    def generate_confirmation_token(self, expiration=3600):
        """生成一个验证用token 持续时间为1天"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """验证token的值"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def get_info(self):
        """返回用户收到的信息"""
        return {'info': self.infos}

    def to_json(self):
        """返回一个json"""
        json_data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'qq': self.qq,
            'WeChat': self.WeChat,
            'name': self.name,
            'nickname': self.nickname,
            'male': self.male,
            'age': self.age,
            'tops': self.tops,
            'weight': self.weight,
            'position': self.position,
            'about_me': self.about_me,
            'avatar_hash': self.avatar_hash
        }
        return json_data

    def easy_to_json(self):
        """返回不保密的用户信息"""
        json_data = {
            'id': self.id,
            'username': self.username,
            'avatar_hash': self.avatar_hash,
            'nickname': self.nickname,
            'position': self.position,
            'about_me': self.about_me,
            'auth_url': url_for('auth.index', id=self.id)
        }
        return json_data

    @staticmethod
    def from_json(data):
        id = data.get('id')
        if id is not None:
            user = User.query.get_or_404(id)
        else:
            user = User()
            user.username = data.get('username')
            user.email = data.get('email')
            user.password = data.get('password')
        user.avatar_hash = data.get('avatar') or user.gravatar()
        user.phone = data.get('phone')
        user.qq = data.get('qq')
        user.WeChat = data.get('WeChat')
        user.name = data.get('name')
        user.nickname = data.get('nickname')
        user.male = int(data.get('gender'))
        user.age = data.get('age')
        user.tops = data.get('tops')
        user.weight = data.get('weight')
        user.about_me = data.get('about_me')
        if user.is_position(data.get('position')):
            user.position = data.get('position')
        return user

    def info_count(self):
        """新消息条目"""
        return len([info for info in self.infos if info.is_read is False])

    def gravatar(self, size=128, default='identicon', rating='g'):
        """使用gravatar生成用户头像"""
        if self.avatar_hash is not None:
            return self.avatar_hash
        if request.is_secure:  # 如果响应是安全的
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        my_hash = hashlib.md5(self.email.encode(
            'utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=my_hash, size=size, default=default, rating=rating
        )

    @staticmethod
    def get_user_id(token):
        """通过token获取用户id"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return data.get('confirm')

    def is_captain(self):
        """返回是否是队长"""
        return self.id == self.team.captain_id


class Info(db.Model):
    """用户接受的信息"""
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def to_json(self):
        json_data = {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message
        }
        return json_data

    @staticmethod
    def from_json(data):
        return Info(user_id=data.get('user_id'), message=data.get('message'))

    def read(self):
        """改变状态为已读"""
        self.is_read = True
        db.session.add(self)


class Team(db.Model):
    """队伍模版"""
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    # 队长id
    captain_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                           unique=True, nullable=True)
    # 队伍名
    name = db.Column(db.String(32), unique=True, nullable=True)
    # 队伍座右铭
    maxim = db.Column(db.String(64))
    # 简介
    about_us = db.Column(db.String(128))
    # 队徽hash
    emblem_hash = db.Column(db.String(128))
    # 队员
    players = db.relationship("User", foreign_keys=[User.team_id],
                              backref='team', lazy='dynamic')
    # 成立时间
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_json(self):
        json_data = {
            'captain': User.query.get(self.captain_id).easy_to_json(),
            'name': self.name,
            'maxim': self.maxim,
            'about_us': self.about_us,
            'emblem_hash': self.emblem_hash,
            'players': [player.easy_to_json() for player in self.players],
            'activities': "#",
            'member_since': self.member_since,
            'count': len([player for player in self.players])
        }
        return json_data

    @staticmethod
    def from_json(data):
        team = Team()
        id = data.get('id')
        if id is not None:
            team = Team.query.get(id)
        if team is not None:
            team.captain_id = data.get('captain_id')
            team.name = data.get('name')
            team.maxim = data.get('maxim')
            team.about_us = data.get('about_us')
            team.emblem_hash = data.get('emblem_hash')
            return team
        return None

    @staticmethod
    def name_is_exist(name):
        """检验队伍名是否存在"""
        team = Team.query.filter_by(name=name).first()
        if team is not None:
            return True
        return False



