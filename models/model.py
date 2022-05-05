from sqlalchemy import Integer, String, Column
from database import Base

class Post(Base):
    __tablename__ = "POSTS"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String, index=True)
    
