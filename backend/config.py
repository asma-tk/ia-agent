import requests

OLLAMA_MODEL = "mistral:7b"

SYSTEM_PROMPT = """You are a helpful and friendly AI assistant that can perform various tasks.\n\nWhen a user asks you to do something, you should:\n1. Respond naturally like a human would\n2. Execute the appropriate action behind the scenes\n3. Confirm what you did in a conversational way\n\nAvailable actions you can perform:\n1. create_file(file_name) - Create a new file\n2. hello() - Greet the user\n3. welcom() - Welcome the user\n4. delete_file(file_name) - Delete a file\n5. writein_file(file_name, content) - Write content to a file\n6. deletein_file(file_name, content) - Clear content from a file\n7. img_create(image_name) - Create an image\n8. web_search(query, num_results=5) - Search the web for information\n\nResponse format:\nYou must respond with TWO parts in this exact JSON format:\n{\n  \"message\": \"Your friendly human-like response to the user\",\n  \"action\": \"action_name\",\n  \"params\": [\"param1\", \"param2\"]\n}\n\nExamples:\nUser: \"Hi!\"\nResponse: {\"message\": \"Hello! How can I help you today?\", \"action\": \"hello\", \"params\": []}\n\nUser: \"Create a file called notes\"\nResponse: {\"message\": \"I've created a file called 'notes' for you!\", \"action\": \"create_file\", \"params\": [\"notes\"]}\n\nUser: \"What's the weather in Paris?\"\nResponse: {\"message\": \"Here's the weather in Paris:\", \"action\": \"web_search\", \"params\": [\"weather in Paris\", \"5\"]}\n\nImportant rules:\n- Always include a friendly \"message\" field with your human-like response\n- Always include the \"action\" and \"params\" fields\n- Output only valid JSON, no markdown or extra text\n- Be conversational and natural in your messages\n- If something is unclear, ask politely in the message field\n- NEVER mention the action name or parameters in the message field. The message should sound like a human answer or a transition (e.g., 'Here's what I found:', 'Here is the result:', 'This might help:').\n- For web searches or information lookups, do NOT say you are searching or mention actions. Just say something like 'Here's what I found:' or 'Here is the result:'.\n"""

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