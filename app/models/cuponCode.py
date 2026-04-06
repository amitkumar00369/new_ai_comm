



from alembic.environment import Column
from sqlalchemy import Integer, String,Boolean

from app.models.base_models import BaseMixin
from core.database import Base


class cupon(Base, BaseMixin):
    __tablename__ = "cupon_codes"
    id = Column(Integer, primary_key=True, index=True)
    cuponId = Column(String, unique=True, index=True)
    code = Column(String, unique=True, index=True)
    discount_percentage = Column(Integer)
    is_active = Column(Boolean, default=True        )