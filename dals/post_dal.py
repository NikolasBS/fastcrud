from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from database.models.post import Post

class PostDAL():
    def __init__(self,db_session:Session):
        self.db_session = db_session
    
    async def create_post(self, title:str, body:str):
        new_post = Post(title=title, body=body)
        self.db_session.add(new_post)
        await self.db_session.flush()
        q = await self.db_session.execute(select(Post).where(Post.title==title,Post.body==body))
        return q.scalars().all()
        
    async def get_all_posts(self) -> List[Post]:
        q = await self.db_session.execute(select(Post).order_by(Post.id))
        return q.scalars().all()
    
    async def get_post(self, id:int):
        q = await self.db_session.execute(select(Post).where(Post.id == id))
        return q.scalars().all()
         
    
    async def update_post(self,id:int, title:Optional[str], body:Optional[str]):
        q = update(Post).where(Post.id == id)
        if title:
            q = q.values(title=title)
        if body:
            q = q.values(body=body)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
        await self.db_session.flush()
        return await self.get_post(id)
    
    async def delete_post(self, id:int):
        q = delete(Post).where(Post.id == id)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
        await self.db_session.flush()
        
    