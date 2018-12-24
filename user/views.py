# coding: utf-8
import asyncio
import json as sjson

from sanic.views import HTTPMethodView
from sanic import Blueprint
from sanic.response import json
from sanic.response import HTTPResponse
from playhouse.shortcuts import model_to_dict
from sanic_openapi import doc
from sanic_jwt.decorators import protected

from .models import *
from config.base_config import *


user_bp = Blueprint('user', url_prefix='/user')
pet_bp = Blueprint('pet', url_prefix='/api/pet')
share_bp = Blueprint('share', url_prefix='/api/share')


class UserView(HTTPMethodView):
    decorators = [protected(), ]

    @doc.summary("Fetches a user by ID")
    @doc.produces({"user": {"name": str, "id": int}})
    async def get(self, request):
        import pdb
        pdb.set_trace()
        name = request.raw_args.get('name', '')
        persons = Person.select()
        if name:
            persons = persons.select().where(Person.name == name)
        persons_list = [model_to_dict(p) for p in persons]
        return HTTPResponse(sjson.dumps(persons_list, default=str))

    async def post(self, request):
        # import pdb
        # pdb.set_trace()
        data = request.form
        post_data = {'name': data.get('name', ''), 'birthday': data.get('birthday', '')}
        persons = Person.create(**post_data)
        # persons = Person.insert_many(**data)
        # persons = [model_to_dict(i) for i in persons]
        # return json(model_to_dict(persons))
        return HTTPResponse(sjson.dumps(persons, default=str))

    def put(self, request):
        pass

    def patch(self, request):
        pass

    def delete(self, request):
        pass


class PetView(HTTPMethodView):

    async def get(self, request):
        # await asyncio.sleep(6)
        pets = Pet.select()
        pets_list = [model_to_dict(p) for p in pets]
        # return json(pets_list)
        # 使用default=str 可以正常序列化时间
        return HTTPResponse(sjson.dumps(pets_list, default=str))


class ShareDetailView(HTTPMethodView):
    """
    分享链接
    """

    @share_bp.get('/<pk>', name='share_detail')
    async def get(self, pk=None):
        """
        获取分享链接详情
        :param self: request
        :param pk:
        :return:
        """
        share = SharePoints.select().where(SharePoints.id == pk).first()
        if share:
            share.click_nums += 1
            share.save()
            serializer = model_to_dict(share)
            return HTTPResponse(sjson.dumps(serializer, default=str))
        return json({}, status=404)

    async def post(self, request):
        """
        创建分享链接
        :param request:
        :return:
        """
        import pdb
        pdb.set_trace()
        data = request.form
        url = data.get('url', '')
        url_type = data.get('url_type', 1)
        user_id = data.get('user_id', 0)
        share = SharePoints.create(
            user_id=user_id, url=url, url_type=url_type, click_nums=0
        )
        serializer = model_to_dict(share)
        return HTTPResponse(sjson.dumps(serializer, default=str), status=201)

    @share_bp.delete('/<pk>', name='delete-share')
    async def delete(self, pk=None):
        """
        删除分享链接
        1. instance 删除
            share.first().delete_instance()
        2. 批量删除
            SharePoints.delete().where(SharePoints.id == pk)
        :param self: request
        :param pk: id
        :return:
        """
        share = SharePoints.delete().where(SharePoints.id == pk)
        return json({'success': True}, status=204)

    @share_bp.get('/list', name='get_all_shares')
    async def get_all_shares(self):
        """
        自定义路由 例子 self=request
        获取所有的分享链接
        :param self:
        :return:
        """
        page = int(self.raw_args.get('page', 1))
        size = int(self.raw_args.get('size', PAGE_SIZE))
        shares = SharePoints.select().order_by(
            '-create_time'
        ).paginate(page, PAGE_SIZE)
        serializer = [model_to_dict(share) for share in shares.iterator()]
        res = {
            'count': shares.count(),
            'page': page,
            'size': size,
            'results': serializer,
        }
        return HTTPResponse(sjson.dumps(res, default=str), status=200)


user_bp.add_route(UserView.as_view(), '/')
pet_bp.add_route(PetView.as_view(), '/')
share_bp.add_route(ShareDetailView.as_view(), '/')



