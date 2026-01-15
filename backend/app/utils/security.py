from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
处理 密码加盐/哈希（不依赖外部环境，纯算法计算）。
"""


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_uuid(version=4):
    """
    生成UUID
    Args:
        version (int): UUID版本,默认为4
    Returns:
        str: 生成的UUID字符串
    Raises:
        ValueError: 当指定的版本不支持时
    """
    if version == 1:
        # 基于时间戳和MAC地址
        generated_uuid = uuid.uuid1()
    elif version == 3:
        # 基于命名空间和名称的MD5哈希
        namespace = uuid.NAMESPACE_DNS
        name = "example.com"
        generated_uuid = uuid.uuid3(namespace, name)
    elif version == 4:
        # 随机生成
        generated_uuid = uuid.uuid4()
    elif version == 5:
        # 基于命名空间和名称的SHA-1哈希
        namespace = uuid.NAMESPACE_DNS
        name = "example.com"
        generated_uuid = uuid.uuid5(namespace, name)
    else:
        raise ValueError(f"不支持的UUID版本: {version}")
    
    return str(generated_uuid)