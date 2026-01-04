from celery import shared_task


@shared_task
def send_welcome_email(email: str):
    # 模拟发送邮件耗时操作
    print(f"Sending welcome email to {email}...")
    return True
