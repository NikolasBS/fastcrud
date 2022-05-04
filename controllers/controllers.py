from fastapi import APIRouter, HTTPException
from models import CrudAPI, arrays, CrudAPIBody

home = APIRouter(prefix="")

@home.get("/")
async def home_home():
    return {"home": "The Homepage"}

@home.get("/crudapi")
async def index():
    return {"arrays":tuple(map(lambda bp : bp.__dict__, arrays))}

@home.get("/crudapi/{id}")
async def show(id:int):
    if len(arrays) < id:
        raise HTTPException(status_code=404, detail="Item not found")
    return arrays[id].__dict__

@home.post("/crudapi")
async def create(array: CrudAPIBody):
    
    arrays.append(CrudAPI(array.title, array.body))
    
    return array.__dict__

@home.api_route("/crudapi/{id}", methods=["Put", "Patch"])
async def update(id: int, array: CrudAPIBody):
    
    if len(arrays) < id:
        raise HTTPException(status_code=404, detail="Item not found")
    
    target = arrays[id]
    target.title = array.title
    target.body = array.body
    
    return target.__dict__

@home.delete("/crudapi/{id}")
async def remove(id: int):
    
    if len(arrays) < id:
        raise HTTPException(status_code=404, detail="Item not found")
    
    array = arrays.pop(id)
    
    return array.__dict__
