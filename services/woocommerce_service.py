from fastapi import HTTPException
from sqlalchemy.orm import Session
from woocommerce import API

from models.store import Store


def get_wc_client(
    user_id: int,
    db: Session
):

    store = db.query(Store).filter(
        Store.user_id == user_id
    ).first()

    if not store:

        raise HTTPException(
            status_code=404,
            detail="WooCommerce store not connected."
        )

    return API(
        url=store.store_url,
        consumer_key=store.consumer_key,
        consumer_secret=store.consumer_secret,
        version="wc/v3",
        timeout=30
    )


def get_store(
    user_id: int,
    db: Session
):

    store = db.query(Store).filter(
        Store.user_id == user_id
    ).first()

    if not store:

        raise HTTPException(
            status_code=404,
            detail="Store not found."
        )

    return store
