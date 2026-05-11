from fastapi import FastAPI
import json
import requests
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


import os
# Always resolve the files directory relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_DIR = os.path.join(BASE_DIR, "files")
from fastapi.staticfiles import StaticFiles
from backend.config import LlamaChat, SYSTEM_PROMPT


app = FastAPI()
#Permet d’accéder aux fichiers du dossier 
app.mount("/files", StaticFiles(directory=FILES_DIR), name="files")

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
   response = requests.get("http://127.0.0.1:8000/openapi.json")
   return response.json()


history=[]

@app.post("/chat")
def chat_endpoint(request: UserRequest):
    try:
        # Ajouter la requête de l'utilisateur à l'historique
        history.append({"role": "user", "content": request.user_input})

        # Inclure l'historique dans les messages envoyés au modèle
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history]

        # Appel de llm pour obtenir l'action à exécuter
        response = chat.get_response(messages)

        # Sauver la reponse du llm dans l'historique pour le prochain tour de conversation
        history.append({"role": "assistant", "content": response})

        # Convertir la reponse du llm en format json pour recuperer l'action et les params
        llm_data = json.loads(response)
        
        # Extract the human-friendly message and action data
        user_message = llm_data.get("message", "Done!")
        action_data = {
            "action": llm_data.get("action"),
            "params": llm_data.get("params", [])
        }

        # Executer l'action de l'agent si une action est fournie
        action_result = None
        if action_data["action"]:
            # Dynamically determine the backend URL for /apply_action
            from fastapi import Request as FastAPIRequest
            try:
                # Try to get the host from the request headers (works in FastAPI >=0.68)
                backend_url = request.headers.get("host", "127.0.0.1:8000")
                scheme = "https" if backend_url.startswith("https") or backend_url.endswith(":443") else "http"
                apply_action_url = f"{scheme}://{backend_url}/apply_action"
            except Exception:
                apply_action_url = "http://127.0.0.1:8000/apply_action"
            agent_response = requests.post(
                apply_action_url,
                json=action_data,
            )
            agent_response.raise_for_status()
            action_result = agent_response.json().get("message", "")

        # For web_search and other actions that return data, append the result to the message
        final_message = user_message
        if action_data["action"] == "web_search" and action_result:
            final_message = f"{user_message}\n\n{action_result}"
        elif action_result and action_data["action"] not in ["create_file", "delete_file", "writein_file", "deletein_file"]:
            final_message = f"{user_message}\n\n{action_result}"

        # Finalement retourne la repense pour le front
        return {
            "status": "success",
            "agent_response": final_message,
            "action": action_data
        }
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"Invalid JSON response from LLM: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
   














