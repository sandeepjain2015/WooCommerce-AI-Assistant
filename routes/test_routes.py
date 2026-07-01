from fastapi import APIRouter
from fastapi import Depends

from auth.dependencies import get_current_user

from models.user import User

router = APIRouter(
    prefix="/test",
    tags=["Test"]
)


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user)
):

    return {

        "id": current_user.id,

        "name": current_user.name,

        "email": current_user.email

    }
