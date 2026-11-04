from fastapi import APIRouter, Request, Response, status

from app.auth import service
from app.auth.dependencies import SESSION_COOKIE_NAME, CurrentUser
from app.auth.schemas import (
    AuthSession,
    EmailCodeLoginRequest,
    EmailCodeSendRequest,
    PasswordLoginRequest,
    PasswordResetRequest,
    PasswordUpdateRequest,
)
from app.config import settings
from app.database import DbDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/email-code", status_code=status.HTTP_204_NO_CONTENT, summary="发送邮箱验证码"
)
def send_email_code(
    request: EmailCodeSendRequest,
    db: DbDep,
    response: Response,
) -> None:
    service.send_email_code(request=request, db=db)

    response.headers["Cache-Control"] = "no-store"


@router.post(
    "/login/email-code",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="邮箱验证码登录",
)
def login_with_email_code(
    request: EmailCodeLoginRequest,
    db: DbDep,
    response: Response,
) -> None:
    session_data = service.login_with_email_code(request=request, db=db)

    _set_session_cookie(response, session_data)


@router.post(
    "/login/password", status_code=status.HTTP_204_NO_CONTENT, summary="密码登录"
)
def login_with_password(
    request: PasswordLoginRequest,
    db: DbDep,
    response: Response,
) -> None:
    session_data = service.login_with_password(request=request, db=db)

    _set_session_cookie(response, session_data)


@router.post(
    "/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="邮箱验证码重置密码",
)
def reset_password(
    request: PasswordResetRequest,
    db: DbDep,
    response: Response,
) -> None:
    service.set_password_with_email_code(
        email=request.email,
        email_code=request.code,
        password=request.password,
        db=db,
    )

    _clear_session_cookie(response)


@router.put(
    "/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="设置或修改密码并更新会话",
)
def set_password(
    request: PasswordUpdateRequest,
    current_user: CurrentUser,
    db: DbDep,
    response: Response,
) -> None:
    session_data = service.set_password_with_email_code(
        email=current_user.email,
        email_code=request.code,
        password=request.password,
        db=db,
    )

    _set_session_cookie(response, session_data)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="退出登录")
def logout(request: Request, response: Response) -> None:
    service.delete_session(session_token=request.cookies.get(SESSION_COOKIE_NAME))

    _clear_session_cookie(response)


def _set_session_cookie(response: Response, session_data: AuthSession) -> None:
    session_token = service.create_session(session_data=session_data)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_token,
        max_age=settings.SESSION_MAX_AGE_SECONDS,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
    )

    response.headers["Cache-Control"] = "no-store"


def _clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
    )

    response.headers["Cache-Control"] = "no-store"
