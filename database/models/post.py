from sqlalchemy import Integer, String, Column
from database import Base

class Post(Base):
    __tablename__ = "POSTS"
    
    id = Column(Integer, primary_key=True, )
    title = Column(String,  nullable=False)
    body = Column(String, nullable=False)
    
