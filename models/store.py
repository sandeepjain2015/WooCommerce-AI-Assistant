from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Store(Base):

    __tablename__ = "stores"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    store_url = Column(
        String,
        nullable=False
    )

    consumer_key = Column(
        String,
        nullable=False
    )

    consumer_secret = Column(
        String,
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="store"
    )