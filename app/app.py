from fastapi import FastAPI
from controllers import home

def create_app():
    
    app = FastAPI()
    app.include_router(home)
    
    return app