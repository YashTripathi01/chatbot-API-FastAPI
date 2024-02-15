from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, text
from sqlalchemy.orm import relationship

from database.engine import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    mobile = Column(String(15), nullable=False)

    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    chat = relationship("Chat", back_populates="users")
