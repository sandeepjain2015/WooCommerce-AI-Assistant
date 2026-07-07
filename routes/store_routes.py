from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.database import get_db

from auth.dependencies import get_current_user

from models.user import User
from models.store import Store

from schemas.store_schema import (
    StoreCreate,
    StoreUpdate
)

router = APIRouter(
    prefix="/store",
    tags=["Store"]
)


@router.post("/connect")
def connect_store(
    request: StoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    existing_store = db.query(Store).filter(
        Store.user_id == current_user.id
    ).first()

    if existing_store:
        raise HTTPException(
            status_code=400,
            detail="Store already connected."
        )

    store = Store(
        user_id=current_user.id,
        store_url=str(request.store_url),
        consumer_key=request.consumer_key,
        consumer_secret=request.consumer_secret
    )

    db.add(store)

    db.commit()

    db.refresh(store)

    return {
        "message": "Store connected successfully."
    }


@router.get("/")
def get_store(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    store = db.query(Store).filter(
        Store.user_id == current_user.id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found."
        )

    return {
	    "id": store.id,
	    "store_url": store.store_url,
	    "connected": True
	}


@router.put("/")
def update_store(
    request: StoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    store = db.query(Store).filter(
        Store.user_id == current_user.id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found."
        )

    store.store_url = str(request.store_url)
    store.consumer_key = request.consumer_key
    store.consumer_secret = request.consumer_secret

    db.commit()

    return {
        "message": "Store updated successfully."
    }


@router.delete("/")
def delete_store(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    store = db.query(Store).filter(
        Store.user_id == current_user.id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found."
        )

    db.delete(store)

    db.commit()

    return {
        "message": "Store removed successfully."
    }
