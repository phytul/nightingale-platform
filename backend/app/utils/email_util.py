from fastapi_mail import FastMail, ConnectionConfig
from pydantic import SecretStr, EmailStr
from app.core import config

def create_qqmail_instance() -> FastMail:
    """创建FastMail实例(每次调用返回新实例,线程/协程安全)"""
    mail_config = ConnectionConfig(
        MAIL_USERNAME=config.MAIL_USERNAME,
        MAIL_PASSWORD=SecretStr(config.MAIL_PASSWORD),
        MAIL_FROM=config.MAIL_FROM,
        MAIL_PORT=config.MAIL_PORT,
        MAIL_SERVER=config.MAIL_SERVER,
        MAIL_FROM_NAME=config.MAIL_FROM_NAME,
        MAIL_STARTTLS=config.MAIL_STARTTLS,
        MAIL_SSL_TLS=config.MAIL_SSL_TLS,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )
    return FastMail(mail_config)