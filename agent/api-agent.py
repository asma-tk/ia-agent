from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import do

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class actionRequest(BaseModel):
    action:str
    params:list




@app.post("/apply_action")
def apply_action(request:actionRequest):
   """Execute action directly when action and params are provided"""

   action=request.action
   params=request.params

   
#recuperer la liste en format de json et faire une boucle pour appliquer les actions
   do([{"action": action, "params": params}])
   return {"message": f"Action {action} applied with params {params}"}
