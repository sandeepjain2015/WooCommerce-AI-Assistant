from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True
    )

    password = Column(
        String,
        nullable=False
    )

    # One User -> Many Stores
    stores = relationship(
        "Store",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
