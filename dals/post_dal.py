from typing import Optional

from database.models.post import Post
from fastapi import HTTPException
from sqlalchemy import delete, update
from sqlalchemy.future import select
from sqlalchemy.orm import Session


class PostDAL():
    def __init__(self,db_session:Session):
        self.db_session = db_session
    
    async def create_post(self, title:str, body:str):
        new_post = Post(title=title, body=body)
        self.db_session.add(new_post)
        await self.db_session.commit()
        key = new_post.id
        await self.db_session.flush()
        return key
    
    async def get_all_posts(self):
        query = await self.db_session.execute(select(Post).order_by(Post.id))
        return query.scalars().all()
            
    async def get_post(self, id:int):
    
        q = await self.db_session.execute(select(Post).where(Post.id == id))
        try:
            values = q.all()[-1]
            keys = q.keys()
        except IndexError:
            await self.db_session.rollback()
            raise HTTPException(status_code=404, detail="Item not found")

        d = {}
        for k, v in zip(keys, values):
            d[k] = v
        return d
        
         
    
    async def update_post(self,id:int, title:Optional[str], body:Optional[str]):
        
        q = await self.db_session.execute(select(Post).where(Post.id == id))
        try:
            values = q.all()[-1]
            keys = q.keys()
        except IndexError:
            await self.db_session.rollback()
            raise HTTPException(status_code=404, detail="Item not found")
        
        
        
        
        
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
        
        q = await self.db_session.execute(select(Post).where(Post.id == id))
        try:
            values = q.all()[-1]
            keys = q.keys()
            print(keys)
        except IndexError:
            await self.db_session.rollback()
            raise HTTPException(status_code=404, detail="Item not found")
        
        
        
        q = delete(Post).where(Post.id == id)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
        await self.db_session.flush()
        
    