# coding: utf-8
import datetime

from peewee import *
# from peewee_async import MySQLDatabase


mysql_db = MySQLDatabase('sanic_demo', user='ivan', password='wh',
                         host='127.0.0.1', port=3306)


class BaseModel(Model):

    class Meta:
        database = mysql_db


class Person(BaseModel):
    name = CharField(max_length=32, null=False, unique=True)
    birthday = DateTimeField(null=True, )


class Pet(BaseModel):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField(max_length=32, null=False, )
    animal_type = IntegerField(choices=((1, 'cat'), (2, 'dog'), (3, 'other')), default=1, null=False)


class User(BaseModel):
    id = PrimaryKeyField()
    name = CharField(
        max_length=64, null=False, verbose_name='姓名')
    password = CharField(
        max_length=128, verbose_name='密码')
    telephone = CharField(
        max_length=11, unique=True, verbose_name='手机号')
    sex = SmallIntegerField(
        default=0, choices=((0, '未知'), (1, '男'), (2, '女')),
        verbose_name='性别')
    address = CharField(
        max_length=64, default='', verbose_name='地址'
    )
    avatar = CharField(
        max_length=128, default='', verbose_name='头像'
    )

    class Meta:
        table_name = 'user'
        indexes = (
            (('telephone', ), True),
        )


class Point(BaseModel):
    """
    用户积分
    """
    user = ForeignKeyField(
        User, verbose_name='用户')
    score = IntegerField(
        default=0, null=False, verbose_name='积分'
    )


class PointRecord(BaseModel):
    """
    积分使用记录
    """
    user = ForeignKeyField(
        User, verbose_name='用户'
    )
    record_type = SmallIntegerField(
        default=0, choices=((0, '环保智库'), (1, '重点行业'), (2, '环保全流程'), (3, '会员兑换'),
                            (4, '分享链接'), (5, '推广注册')),
        verbose_name='使用类型'
    )
    score = SmallIntegerField(
        default=0, verbose_name='积分'
    )
    type_id = IntegerField(
        default=0, verbose_name='积分使用对象'
    )

    class Meta:
        table_name = 'point_record'
        indexes = (
            (('record_type', ), True),
            (('type_id', ), True),
        )


class SharePoints(BaseModel):
    """
    用户分享链接记录
    """
    user_id = IntegerField(
        default=0, verbose_name='分享用户id'
    )
    url = CharField(
        default='', max_length=256, verbose_name='分享链接'
    )
    url_type = IntegerField(
        default=1, choices=((1, '页面链接'), (2, '注册链接')),
        verbose_name='链接类型'
    )
    create_time = DateTimeField(
        default=datetime.datetime.now(), verbose_name='创建时间'
    )
    click_nums = IntegerField(
        default=0, verbose_name='点击数量'
    )

    class Meta:
        table_name = 'share_points'
        indexes = (
            (('user_id', ), True),
        )


class ShareClickRecord(BaseModel):
    """
    分享链接被点击记录
    """
    share_points = ForeignKeyField(
        SharePoints, verbose_name='分享链接'
    )
    click_time = DateTimeField(
        default=datetime.datetime.now(), verbose_name='点击时间'
    )
    ip = IPField(
        verbose_name='点击ip地址'
    )
    user_id = IntegerField(
        default=0, verbose_name='用户id'
    )

    class Meta:
        table_name = 'share_click_record'
        indexes = (
            (('url', ), True),
            (('user_id', ), True),
        )


# mysql_db.connection()
# mysql_db.create_tables([User, Point, PointRecord])


