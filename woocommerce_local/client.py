from woocommerce import API

from context.request_context import (
    get_current_user,
    get_db,
)

from models.store import Store


class WooCommerceClient:

    @staticmethod
    def client():

        user = get_current_user()

        db = get_db()

        if user is None:
            raise HTTPException(status_code=401, detail="User not authenticated.")

        store = db.query(Store).filter(Store.user_id == user.id).first()

        if store is None:
            raise HTTPException(status_code=404, detail="Store not connected.")

        return API(
            url=store.store_url,
            consumer_key=store.consumer_key,
            consumer_secret=store.consumer_secret,
            version="wc/v3",
            timeout=30
        )