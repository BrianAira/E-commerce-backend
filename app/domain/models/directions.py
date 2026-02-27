
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from app.core.database import Base


class Directions(Base):
    __tablename__="directions"
    
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    street_address=Column(String(255), nullable=False)
    city=Column(String(255), nullable=False)
    state=Column(String(255), nullable=False)
    postal_code=Column(String(20), nullable=False)
    country=Column(String(255), nullable=False)
    
    # shipping_address=Column(String(500), default="", index=True)
    additional_info=Column(String(500), nullable=True)
    
    user=relationship("User", back_populates="directions")
    
    