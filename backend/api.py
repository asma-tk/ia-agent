from fastapi import FastAPI
import json
import requests
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from fastapi.staticfiles import StaticFiles
from config import LlamaChat, SYSTEM_PROMPT


app = FastAPI()
#Permet d’accéder aux fichiers du dossier 
app.mount("/files", StaticFiles(directory="../files"), name="files")
chat = LlamaChat()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_methods=["*"],
   allow_headers=["*"],
)


class UserRequest(BaseModel):
   user_input: str


# obtenir la documentation
@app.get("/apply_action")
def apply_action():
   response = requests.get("http://127.0.0.1:8002/openapi.json")
   return response.json()

history=[]
@app.post("/chat")
def chat_endpoint(request: UserRequest):
   try:
      # context 
      # liste et description des actions
      # explication pour le llm de ce qu'il doit faire
      # historique de la conversation
    
    #engistrer la reponse du llm pour le prochain tour de conversation
      
      # Ajouter la requête de l'utilisateur à l'historique


       history.append({"role": "user", "content": request.user_input})

       # Inclure l'historique dans les messages envoyés au modèle

       messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history] 
      
      #apelle de llm pour obtenir l'action à exécuter

       response=chat.get_response(messages)

       #sauver la reponse du llm dans l'historique pour le prochain tour de conversation

       history.append({"role": "assistant", "content": response})



     #convertir la reponse du llm en format json pour recuperer l'action et les params
       action_data = json.loads(response)


       #executer L'action de l'agent et recuperer la reponse de l'action
       agent_response = requests.post(
       "http://127.0.0.1:8002//apply_action",
        json=action_data,
       )
       agent_response.raise_for_status()  # Vérifie si la requête a réussi
       agent_playload = agent_response.json()

       return {
          "status": "success",
            "agent_response": agent_playload.get("message", "action applied successfully"),
            "action": action_data
       }
   except json.JSONDecodeError:
       return {"status": "error", "message": "Invalid JSON response from LLM","raw": response}
   except Exception as e:
       return {"status": "error", "message": str(e)}
       #
   














