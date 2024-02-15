from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    text,
)
from sqlalchemy.orm import relationship

from database.engine import Base


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)

    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    users = relationship("User", back_populates="chat")
