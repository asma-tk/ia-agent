from fastapi import FastAPI
import json
import requests
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from fastapi.staticfiles import StaticFiles
from config import LlamaChat, SYSTEM_PROMPT


app = FastAPI()
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


@app.get("/apply_action")
def apply_action():
   response = requests.get("http://127.0.0.1:8000/openapi.json")
   return response.json()


@app.post("/chat")
def chat_endpoint(request: UserRequest):
   try:
      messages = [
         {"role": "system", "content": SYSTEM_PROMPT},
         {"role": "user", "content": request.user_input},
      ]
      response = chat.get_response(messages)
      action_data = json.loads(response)

      agent_response = requests.post(
         "http://127.0.0.1:8000/apply_action",
         json=action_data,
      )
      agent_response.raise_for_status()
      agent_payload = agent_response.json()

      return {
         "status": "success",
         "response": agent_payload.get("message", "Action executed"),
         "action": action_data,
      }
   except json.JSONDecodeError:
      return {"status": "error", "message": "Model response is not valid JSON", "raw": response}
   except Exception as e:
      return {"status": "error", "message": str(e)}


