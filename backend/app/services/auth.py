import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
from enum import Enum
from app.core import config
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from threading import Lock

"""
这段代码实现了一个基于 JWT (JSON Web Token) 的认证系统，
采用单例模式设计，用于 FastAPI 应用。
核心功能包括生成和验证访问令牌(Access Token)和刷新令牌(Refresh Token)
pyjwt版本:pip install pyjwt==2.10.1
"""

class SingletonMeta(type):
    """
    单例模式
    """
    _instances = {} # 存储唯一实例
    _lock: Lock = Lock() # 保证多线程安全 

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class TokenTypeEnum(Enum):
    """
    令牌类型枚举
    """
    ACCESS_TOKEN = 1 # 访问令牌
    REFRESH_TOKEN = 2 # 刷新令牌


# 单例设计模式
class AuthHandler(metaclass=SingletonMeta):
    """
    单例类,封装所有JWT操作
    """
    security = HTTPBearer() # 创建HTTP Bearer认证方案实例
    secret = config.JWT_SECRET_KEY

    def _encode_token(self, user_id: int, type: TokenTypeEnum):
        """
        生成JWT令牌
        """
        payload = dict(
            iss=user_id, # 签发者（用户ID）
            sub=str(type.value) # 主题（令牌类型）
        )
        to_encode = payload.copy() # 创建负载副本
        if type == TokenTypeEnum.ACCESS_TOKEN: # 如果是访问令牌
            exp = datetime.now() + config.JWT_ACCESS_TOKEN_EXPIRES
        else:
            exp = datetime.now() + config.JWT_REFRESH_TOKEN_EXPIRES
        to_encode.update({"exp": int(exp.timestamp())}) # 添加过期时间戳到负载（exp申明）
        return jwt.encode(to_encode, self.secret, algorithm='HS256') #使用HS256算法编码JWT并返回

    def encode_login_token(self, user_id: int):
        """
        生成登陆令牌对（访问令牌+刷新令牌）
        """
        access_token = self._encode_token(user_id, TokenTypeEnum.ACCESS_TOKEN)
        refresh_token = self._encode_token(user_id, TokenTypeEnum.REFRESH_TOKEN)
        login_token = dict(
            access_token=f"{access_token}",
            refresh_token=f"{refresh_token}"
        )
        return login_token

    def encode_update_token(self, user_id):
        """
        生成更新令牌（仅访问令牌）
        """
        access_token = self._encode_token(user_id, TokenTypeEnum.ACCESS_TOKEN)

        update_token = dict(
            access_token=f"{access_token}"
        )
        return update_token

    def decode_access_token(self, token):
        """
        解码访问令牌
        """
        # ACCESS TOKEN：不可用（过期，或有问题），都用403错误
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256']) # 尝试解码令牌
            if payload['sub'] != str(TokenTypeEnum.ACCESS_TOKEN.value):
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Token类型错误！')
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Access Token已过期！')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Access Token不可用！')

    def decode_refresh_token(self, token):
        # REFRESH TOKEN：不可用（过期，或有问题），都用401错误
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if payload['sub'] != str(TokenTypeEnum.REFRESH_TOKEN.value):
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Token类型错误！')
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Refresh Token已过期！')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Refresh Token不可用！')

    def auth_access_dependency(self, auth: HTTPAuthorizationCredentials = Security(security)):
        # 验证访问令牌
        return self.decode_access_token(auth.credentials) # 调用解码方法并返回用户ID

    def auth_refresh_dependency(self, auth: HTTPAuthorizationCredentials = Security(security)):
        # 验证刷新令牌
        return self.decode_refresh_token(auth.credentials) # 调用解码方法并返回用户ID