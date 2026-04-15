import requests

OLLAMA_MODEL = "mistral:7b"

SYSTEM_PROMPT = """You are an action-selection assistant for a file task chatbot.

Your job is to convert a user's request into exactly one valid action and its parameters.

Available actions:
1. create_file(file_name)
2. delete_file(file_name)
3. writein_file(file_name, content)
4. deletein_file(file_name, content)

Rules:
- Return only one action.
- Use only the actions listed above.
- Preserve the exact action names.
- If the request is unclear, missing a file name, or missing content, ask for the missing information.
- If the user wants to clear the content of a file without deleting the file, use deletein_file.
- If the user wants to remove the entire file, use delete_file.
- Output must be valid JSON only.

Output format:
{"action": "action_name", "params": ["param1", "param2"]}
"""

class LlamaChat:
    def get_response(self, messages):

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False
                
            }
        )

        data = response.json()
        return data["message"]["content"]