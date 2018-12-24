# coding: utf-8
from sanic_jwt import Configuration

from .models import *


class CustomConfiguration(Configuration):
    """
    自定义jwt配置
    authorization_header_prefix:
    jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTQ0MDg2MTA3fQ.wvnkpKzHVyRfgRtSpCJrh72Tx4n6vJLJFT_qg
    """
    access_token_name = 'jwt'
    authorization_header_prefix = 'jwt'
    secret = '801d5b47a06e4ee6aab457e3de4fb8a6'
    user_id = 'id'
    expiration_delta = 60 * 5 * 6
