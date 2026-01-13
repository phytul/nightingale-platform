
from redis.asyncio import Redis
import redis
import json
import time
from typing import Optional, Dict, Any
from app.core.config import EXPIRE_TIMES

class CaptchaStorage:
    """验证码存储服务 - 生产级实现"""
    
    def __init__(self,session: Redis):
        self.redis_client = session
        
    def _get_client_ip(self) -> str:
        """
        获取客户端IP（需要根据实际框架实现）
        在实际使用中，这个方法应该从请求上下文中获取IP
        """
        # 这里只是一个示例，实际使用时需要根据Web框架调整
        return "127.0.0.1"
    
    def store_email_code(self, email: str, code: str, scene: str = "register") -> bool:
        """
        存储邮箱验证码
        scene: register/login/reset_password/bind_email
        """
        try:
            key = f"captcha:email:{scene}:{email}"
            data = {
                "code": code,
                "created_at": int(time.time()),
                "ip": self._get_client_ip(),
                "scene": scene
            }
            expire_seconds = EXPIRE_TIMES.get(scene, 300)
            self.redis_client.setex(key, expire_seconds, json.dumps(data))
            return True
            
        except redis.RedisError as e:
            print(f"Redis错误 - 存储邮箱验证码失败: {e}")
            return False
        except Exception as e:
            print(f"未知错误 - 存储邮箱验证码失败: {e}")
            return False
    
    def verify_email_code(self, email: str, code: str, scene: str = "register") -> Dict[str, Any]:
        """验证邮箱验证码"""
        try:
            key = f"captcha:email:{scene}:{email}"
            data_str = self.redis_client.get(key)
            
            if not data_str:
                return {"success": False, "message": "验证码已过期或不存在"}
            
            data = json.loads(data_str)
            
            # 验证码匹配
            if data["code"] == code:
                self.redis_client.delete(key)
                self._clear_violations(email)
                print(f"邮箱验证码验证成功: {email}, scene: {scene}")
                return {"success": True, "message": "验证成功"}
            else:
                print(f"邮箱验证码验证失败: {email}, 请重新获取验证码")
                return {
                    "success": False, 
                    "message": f"验证码错误，请重新获取验证码"
                }
        except json.JSONDecodeError as e:
            print(f"JSON解析错误 - 验证邮箱验证码异常: {e}")
            self.redis_client.delete(key)
            return {"success": False, "message": "验证码数据异常"}
        except redis.RedisError as e:
            print(f"Redis错误 - 验证邮箱验证码异常: {e}")
            return {"success": False, "message": "系统繁忙，请稍后重试"}
        except Exception as e:
            print(f"未知错误 - 验证邮箱验证码异常: {e}")
            return {"success": False, "message": "验证过程出现异常"}