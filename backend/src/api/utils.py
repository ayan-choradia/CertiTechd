
from fastapi import APIRouter

# from src.core.celery_app import celery_app


# from src.utils import send_test_email


router = APIRouter()


# @router.post("/test-celery/", response_model=Msg, status_code=201)
# async def test_celery(
#     msg: Msg,
#     current_user: User = Depends(get_current_active_superuser),
# ) -> Any:
#     """
#     Test Celery worker.
#     """
#     celery_app.send_task("app.worker.test_celery", args=[msg.msg])
#     return {"msg": "Word received"}


# @router.post("/test-email/", response_model=Msg, status_code=201)
# async def test_email(
#     email_to: EmailStr,
#     current_user: User = Depends(get_current_active_superuser),
# ) -> Any:
#     """
#     Test emails.
#     """
#     send_test_email(email_to=email_to)
#     return {"msg": "Test email sent"}


def to_lower_camel(string: str) -> str:
    """
    Changes snake_case to lower camel case

    Input:
    -------
    string: str
        The snake_case string

    Output:
    --------
    str -> The lowerCamelCase string
    """
    return "".join(
        word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_"))
    )
