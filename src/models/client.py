from sqlalchemy import Column, BigInteger, String, Text, DateTime
from src.modules.database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    telegram = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Client {self.name}>"
