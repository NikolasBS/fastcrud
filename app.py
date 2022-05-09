import uvicorn
from configuration.config import variables as config
from fastapi import FastAPI
from database.config import engine, Base
from view import post_view


app = FastAPI()
app.include_router(post_view.router)
 
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)    
    
if __name__ == "__main__":
    uvicorn.run("app:app", port=int(config["PORT"]))