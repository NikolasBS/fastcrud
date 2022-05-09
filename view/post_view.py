from typing import Optional

from fastapi import APIRouter, Depends

from dependencies.get_post_dal import get_post_dal 
from dals import PostDAL

router = APIRouter()

@router.post("/post")
async def create_post(title:str, body:str, post_dal: PostDAL = Depends(get_post_dal)):
    return await post_dal.create_post(title, body)

@router.get("/post")
async def get_all_posts(post_dal: PostDAL = Depends(get_post_dal)):
  return await post_dal.get_all_posts()

@router.put("/post/{post_id}")
async def update_post(post_id:int, title:Optional[str], body:Optional[str], post_dal: PostDAL = Depends(get_post_dal)):
    return await post_dal.update_post(post_id, title, body)

@router.delete("/post/{post_id}")
async def delete_post(post_id:int, post_dal: PostDAL = Depends(get_post_dal)):
    return await post_dal.delete_post(post_id)
@router.get("/post/{post_id}")
async def get_post(post_id: int, post_dal: PostDAL = Depends(get_post_dal)):
    return await post_dal.get_post(post_id)
