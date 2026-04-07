
from sqlalchemy import Column, Integer, String, ForeignKey, Text,Enum
from sqlalchemy.orm import relationship

from app.models.base_models import BaseMixin
from core.database import Base
from app.utils.enum import senderType

class Message(Base, BaseMixin):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    messageId = Column(String, unique=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    sender = Column(Enum(senderType), unique=True)  # "user" / "ai"
    message_text = Column(Text)

    # conversation = relationship("Conversation", back_populates="messages")