from pydantic import BaseModel

class CrudAPI:
    title = ""
    body = ""

    def __init__(self, title, body):
        self.title = title
        self.body = body

arrays = []

test = CrudAPI("Testing", "Testbody")

class CrudAPIBody(BaseModel):
    title:str
    body:str

arrays.append(test)