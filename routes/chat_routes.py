from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database.database import get_db
from models.user import User

from schemas.chat_schema import ChatRequest
from services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


@router.post("/")
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    response = ChatService.chat(
        message=request.message,
        current_user=current_user,
        db=db
    )

    return {
        "response": response
    }