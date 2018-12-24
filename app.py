# coding: utf-8
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import RequestTimeout, ServiceUnavailable, SanicException
from sanic import response
from sanic_cors import CORS
from sanic_openapi import swagger_blueprint, openapi_blueprint
from sanic_jwt import Initialize
from sanic_session import Session, InMemorySessionInterface

from user.views import *
from config import base_config
from user.utils import CustomConfiguration


async def authenticate(request):
    """
    获取要加密的数据, 返回字典且必须有个user_id属性,
    然后将此字典进行加密生成token
    :param request:
    :return:
    """
    import pdb
    pdb.set_trace()
    user = model_to_dict(Person.select().first())
    user['user_id'] = user.get('id')
    return user


async def retrieve_user(request, payload, *args, **kwargs):
    """
    token认证通过后,根据token中的数据获取用户对象
    :param request:
    :param payload:
    :param args:
    :param kwargs:
    :return:
    """
    if payload:
        user_id = payload.get('user_id', None)
        user = Person.select().where(Person.id == user_id).first()
        return model_to_dict(user)
    else:
        return None

app = Sanic(__name__)
session = Session(app, interface=InMemorySessionInterface)
# 跨域处理
CORS(app, automatic_options=True)
# Initialize(
#     app,
#     authenticate=authenticate,
#     access_token='jwt',
#     authorization_header_prefix='jwt',
#     retrieve_user=retrieve_user
# )
Initialize(
    app,
    authenticate=authenticate,
    configuration_class=CustomConfiguration
)
app.config['WTF_CSRF_SECRET_KEY'] = 'top secret!'

# session = {'sanic_uuid': '234324dfdf'}


# @app.middleware('request')
# async def custom_add_session_to_request(request):
#     """
#     add session to request
#     :param request:
#     :return:
#     """
#     import pdb
#     pdb.set_trace()
#     request['session'] = {'funck': 'dfdfd3434'}


@app.exception(ServiceUnavailable)
def custom_response_timeout_error(request, exception):
    return response.text('连接超时', 503)


@app.exception(RequestTimeout)
def custom_request_timeout_error(request, exception):
    return response.text('request time out', 408)


@app.middleware('request')
def block_ip(request):
    # 返回HTTPResponse时，则停止往下继续运行
    black_list = []
    if request.ip in black_list:
        return response.text('您的ip已被锁定', 503)


@app.middleware('response')
async def add_header(request, response):
    response.headers['content-type'] = 'application/json'


app.blueprint(user_bp)
app.blueprint(pet_bp)
app.blueprint(share_bp)
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

app.config.from_object(base_config)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8001, debug=True)
