
class CaptchaDataStructure:
    """验证码数据结构设计"""
    
    # 主要键模式
    EMAIL_CAPTCHA_KEY = "cap:e:{scene}:{email}"      # 邮箱验证码
    SMS_CAPTCHA_KEY = "cap:s:{scene}:{phone}"        # 短信验证码  
    VOICE_CAPTCHA_KEY = "cap:v:{scene}:{phone}"      # 语音验证码
    EMAIL_VERIFY_KEY = "cap:ev:{email}"              # 邮箱验证链接
    RESET_TOKEN_KEY = "cap:rt:{email}"               # 重置密码令牌
    
    # 频率限制键模式
    RATE_LIMIT_IP = "rl:ip:{ip}:{date}"             # IP频率限制
    RATE_LIMIT_PHONE = "rl:ph:{phone}:{hour}"       # 手机号频率限制
    RATE_LIMIT_EMAIL = "rl:em:{email}:{hour}"       # 邮箱频率限制
    
    # 黑名单键模式  
    BLACKLIST_IP = "bl:ip:{ip}"                     # IP黑名单
    BLACKLIST_PHONE = "bl:ph:{phone}"               # 手机号黑名单
    BLACKLIST_EMAIL = "bl:em:{email}"               # 邮箱黑名单
    
    # 统计数据键模式
    STATS_HOURLY = "stats:cap:{type}:{scene}:{hour}" # 小时统计
    STATS_DAILY = "stats:cap:{type}:{scene}:{date}" # 日统计

# 具体数据示例
email_captcha_example = {
    # 验证码核心数据
    "code": "123456",
    "code_hash": "a1b2c3d4e5f6",  # 哈希后的验证码，更安全
    
    # 元数据
    "created_at": 1698765432,
    "expire_at": 1698766032, 
    "attempts": 0,
    "max_attempts": 5,
    
    # 安全信息
    "security": {
        "ip": "192.168.1.100",
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
        "device_fingerprint": "abc123def456",
        "geo_location": "CN-BJ"
    },
    
    # 业务信息
    "business": {
        "scene": "register",  # register/login/reset_password/bind_email
        "priority": "normal", # low/normal/high
        "source": "web",      # web/mobile/app/api
        "campaign_id": "new_user_promo_2024"
    },
    
    # 状态信息
    "status": {
        "sent": True,
        "delivered": True, 
        "read": False,
        "used": False
    }
}

sms_captcha_example = {
    "code": "789012",
    "code_hash": "f6e5d4c3b2a1",
    "created_at": 1698765432,
    "expire_at": 1698765732,  # 短信验证码通常更短
    "attempts": 0,
    "max_attempts": 3,  # 短信验证码尝试次数更少
    
    "security": {
        "ip": "192.168.1.100",
        "phone": "13800138000",
        "operator": "mobile",  # mobile/unicom/telecom
        "region": "beijing"
    },
    
    "business": {
        "scene": "login",
        "sms_template": "login_template_v2",
        "sms_provider": "aliyun"  # aliyun/tencent/huawei
    }
}