
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import do
import json
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ActionRequest(BaseModel):
    action: str
    params: list


class ChatRequest(BaseModel):
    user_input: str

AVAILABLE_ACTIONS = [
    "create_file", "delete_file", "writein_file",
    "deletein_file", "hello", "welcom",
    "img_create", "web_search"
]

@app.post("/apply_action")
def apply_action(request: ActionRequest):
    """Execute action directly when action and params are provided"""
    result = do([{"action": request.action, "params": request.params}])
    return {"message": result}



@app.post("/chat")
def chat(request: ChatRequest):
    """Parse natural language input and execute the corresponding action using Ollama"""
    OLLAMA_URL = "http://localhost:11434/api/generate"  # Change if your Ollama server is remote
    OLLAMA_MODEL = "llama3"  # Change to your preferred model name

    system_prompt = f"""You are an agent that maps natural language to actions.
Available actions: {json.dumps(AVAILABLE_ACTIONS)}

Given a user message, respond ONLY with a valid JSON object in this exact format:
{{"action": "<action_name>", "params": [<param1>, <param2>, ...]}}

Rules:
- "create_file" needs one param: the file name (string, no extension needed)
- "delete_file" needs one param: the file name
- "writein_file" needs two params: file_name, content (string)
- "deletein_file" needs two params: file_name, content (leave content empty string "")
- "img_create" needs one param: image name
- "web_search" needs one param: the search query string
- "hello" and "welcom" need no params: []
- If you cannot map the input to an action, respond with: {{"action": "hello", "params": []}}

Do not include any explanation or extra text. Only the JSON object."""

    prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{request.user_input}\n<|assistant|>"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        result_json = response.json()
        raw = result_json.get("response", "").strip()
        parsed = json.loads(raw)
        action = parsed["action"]
        params = parsed["params"]
        result = do([{"action": action, "params": params}])
        return {
            "status": "success",
            "action": action,
            "params": params,
            "message": str(result) if result is not None else f"Action '{action}' executed successfully."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to parse or execute action: {str(e)}",
            "raw_llm_output": raw if 'raw' in locals() else None
        }