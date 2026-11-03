"""通过 Resend 同步发送验证码邮件。"""

import logging

import resend
from resend.exceptions import ResendError

from app.auth.exceptions import EmailSendError
from app.auth.schemas import EmailCodePurpose
from app.config import settings

logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY.get_secret_value()
resend.default_http_client = resend.RequestsClient(timeout=10)


def send_verification_email(
    *, email: str, purpose: EmailCodePurpose, email_code: str
) -> None:
    if purpose == "email_login":
        email_purpose = "登录"
    else:
        email_purpose = "设置密码"

    email_message: resend.Emails.SendParams = {
        "from": f"{settings.PROJECT_NAME} <{settings.EMAIL_FROM}>",
        "to": [email],
        "subject": f"{email_purpose}验证码",
        "html": f"<p>你的{email_purpose}验证码：<strong>{email_code}</strong></p>"
        "<p>10 分钟内有效，请勿向他人透露。</p>",
    }

    try:
        resend.Emails.send(email_message)
    except ResendError as error:
        logger.error(
            "验证码邮件发送失败：类型=%s，状态=%s", error.error_type, error.code
        )
        raise EmailSendError from None
