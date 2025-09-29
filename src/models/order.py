from sqlalchemy import Column, BigInteger, String, Text, DateTime, Numeric
from src.modules.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(BigInteger, primary_key=True, index=True)
    client_id = Column(BigInteger, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), default="new")
    created_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Order {self.title} - {self.amount}>"
