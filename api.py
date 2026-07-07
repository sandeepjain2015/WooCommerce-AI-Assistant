from fastapi import FastAPI

from database.database import Base, engine

import models.user
import models.store

from routes.auth_routes import router as auth_router
from routes.store_routes import router as store_router
from routes.test_routes import router as test_router
from routes.chat_routes import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(test_router)
app.include_router(store_router)
app.include_router(chat_router)


@app.get("/")
def home():

    return {
        "message": "WooCommerce AI Assistant API"
    }
