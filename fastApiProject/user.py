import asyncio
import traceback
from time import time

import jwt
from authing import AuthenticationClient
from authing import ManagementClient

from database.models import my_redis


class AuthingServer:
    # Authing 应用 ID
    __app_id = '62fc94595854df71f7bbe61e'
    # Authing 应用密钥
    __app_secret = '64e383696b6af199003057722e1b93fb'
    # Authing 应用地址，如 https://example.authing.cn
    __app_host = 'https://chuxiaodong-yyzqtyswzhxt.authing.cn'
    # Authing 应用配置的登录回调地址
    __redirect_uri = 'http://localhost:5173/'
    __verily_id_token_url = "https://chuxiaodong-yyzqtyswzhxt.authing.cn/api/v2/oidc/validate_token"
    # JWKS 公钥端点
    __jwks_link = "https://chuxiaodong-yyzqtyswzhxt.authing.cn/oidc/.well-known/jwks.json"
    __public_key = {  # 从 JWKS 公钥端点获取的公钥
        "kty": "RSA",
        "e": "AQAB",
        "n": "ts4oLuSiiv9BJGfi7Oq_n97c570nMftcCpq1K9iNH4VkxSjZfPmQfZsugWFfDYlktqAPkclpVRe7ZKhLlELkrJLf_MRt7QpYgFOieV52dRugRH25zCMCtRM8wdsVNMB8kWZPMnG8EDu7nlsgZFEsjl6UBVkkMwz-4nBHkk2u7q2G7Lp4wdm8702HZP3D2oOwXOgfEGBc2k45nzosDjEYLdJMoPhSWEjVaJGk5895L83FKJz9D3eXGHAWlgKjV3CJcxkZaAbj9aENpxMrIiVokgwNmqWHC7QeFFoUZYVY7Z-BVkq3m0z3Yna5-0MbuhAMN8Xgg8CwCzCm3trQRaHt_Q",
        "alg": "RS256",
        "use": "sig",
        "kid": "3Ip6WHv6heULpKFAyQPIxddzWOvwr7kjtUkIXMgjJos"
    }
    __issuer = "https://chuxiaodong-yyzqtyswzhxt.authing.cn/oidc"
    # 用户池
    __access_key_id = "62fc94594fdc1262a1b37033"
    __access_key_secret = "ba5d47dd5e5c4611210386d6e52319c4"
    __authentication_client = AuthenticationClient(__app_id, __app_secret, __app_host, __redirect_uri)
    __management_client = ManagementClient(__access_key_id, __access_key_secret)

    def __init__(self):
        pass

    def get_login_url(self):
        # 获取登录 URL
        url = self.__app_host
        return url

    def get_token_by_code(self, code):
        try:
            # 使用 code 获取 token
            token = self.__authentication_client.get_access_token_by_code(code)
            return token
        except:
            traceback.print_exc()
            return ""

    def log_out(self, token):
        success = self.__authentication_client.revoke_token(token)
        return success

    def verify_id_token_hs256(self, token):
        if token is None or len(token) < 20:
            return None
        try:
            decoded = jwt.decode(token, self.__app_secret, algorithms=["HS256"], audience=self.__app_id)
            current_time = time()
            if current_time < decoded['exp']:
                authing_id = decoded['sub']
                if authing_id:
                    re_d = {'authing_id': authing_id,
                            'email': decoded['email'],
                            'phone': decoded['phone_number']
                            }
                    my_redis.set(token, re_d['authing_id'], ex=3600)
                    return re_d
        except:
            pass
        return None

    def verify_id_token_hs256_redis(self, token):
        if token is None or len(token) < 20:
            return None
        if my_redis.exists(token):
            return my_redis.get(token)
        try:
            decoded = jwt.decode(token, self.__app_secret, algorithms=["HS256"], audience=self.__app_id)
            current_time = time()
            if current_time < decoded['exp']:
                authing_id = decoded['sub']
                if authing_id:
                    my_redis.set(token, authing_id, ex=3600)
                    return authing_id
        except:
            pass
        return None

    def get_authing_id_by_access(self, token):
        # 获取用户 ID
        user = self.__authentication_client.get_user_info_by_access_token(token)
        return user

    def get_all_user_id(self):
        # 获取用户列表
        users = self.__management_client.list_users()
        return users['data']['list']

    def del_user(self, user_id):
        # 删除用户
        self.__management_client.delete_users_batch([user_id])


authing_server = AuthingServer()


async def del_test_user():
    user_list = authing_server.get_all_user_id()
    for i in range(len(user_list)):
        user_i = user_list[i]
        if user_i['phone'] == '18648268144':
            authing_server.del_user(user_i['userId'])
            from database.delete_data import delete_user
            await delete_user(user_i['userId'])
            break


if __name__ == '__main__':
    asyncio.run(del_test_user())
    print(0)
