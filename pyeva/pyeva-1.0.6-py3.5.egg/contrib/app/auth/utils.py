from eva.mail.sendcloud import SendCloud
from eva.conf import settings


def identifier_notice_email(to_addr, code):
    """邮件通知验证码"""
    mds = SendCloud(
        api_user=settings.SENDCLOUD_API_USER,
        api_key=settings.SENDCLOUD_API_KEY,
        from_addr=settings.EMAIL_FROM_ADDR,
        fromname=settings.EMAIL_FROM_NAME,
        replyto=settings.EMAIL_REPLAY_TO)
    mds.template_send(
        template_name=settings.EMAIL_AUTHCODE_TEMPLATE,
        subject=settings.EMAIL_AUTHCODE_SUBJECT,
        sub_vars={
            "to": [to_addr],
            "sub": {
                "%name%": [to_addr],
                "%authcode%": [code],
            },
        })
