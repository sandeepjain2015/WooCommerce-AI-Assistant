from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.database import get_db

from models.user import User

from schemas.auth_schema import RegisterRequest
from schemas.auth_schema import LoginRequest

from auth.hashing import hash_password
from auth.hashing import verify_password

from auth.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    new_user = User(

        name=request.name,

        email=request.email,

        password=hash_password(
            request.password
        )
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {

        "message": "Registration successful."
    }


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
        )

    if not verify_password(
        request.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
        )

    token = create_access_token(

        {
            "sub": user.email
        }
    )

    return {

        "access_token": token,

        "token_type": "bearer"
    }
