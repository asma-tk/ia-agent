import requests

OLLAMA_MODEL = "mistral:7b"

SYSTEM_PROMPT = """You are an action-selection assistant for a file task chatbot.

Your job is to convert a user's request into exactly one valid action and its parameters.

Available actions:
1. create_file(file_name)
2. hello()
3. welcom()
4. delete_file(file_name)
5. writein_file(file_name, content)
6. deletein_file(file_name, content)
7. img_create(image_name)

Rules:
- Return only one action.
- Use only the actions listed above.
- Preserve the exact action names.
- If the request is unclear, missing a file name, or missing content, ask for the missing information.
- If the user wants to clear the content of a file without deleting the file, use deletein_file.
- If the user wants to remove the entire file, use delete_file.
- If the user asks to download a file, always return the file with the last modification added.
- "create_file" is ONLY for creating new empty files.

Output format:
{"action": "action_name", "params": ["param1", "param2"]}

Important:
- Output only valid JSON. Do not add any explanation, markdown, or text outside the JSON object.
- Never use markdown or code blocks.
- Your response must be a single JSON object, nothing else.
"""

class LlamaChat:
    def get_response(self, messages):

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages, # List of dicts with "role" and "content"
                "stream": False # cette option est pour dire que je veux pas de stream de reponse du llm mais plutot une reponse complete a la fin, c'est plus simple pour le parsing du json et l'execution de l'action
                
            }
        )

        data = response.json() # Assuming the response is in JSON format and has a "message" field with "content"
        return data["message"]["content"] #content cest le texte de la reponse du llm qui contient l'action a executer en format json