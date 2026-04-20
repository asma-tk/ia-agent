from config import LlamaChat, SYSTEM_PROMPT
import json
import sys
sys.path.append('../agent')
from agent import do

def main():
    print("Llama LLM Chat - Type 'exit' to quit.")

    chat = LlamaChat()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]: 
            print("\nExiting. Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        response = chat.get_response(messages)

        messages.append({"role": "assistant", "content": response})

        print(f"Llama: {response}")

        # Exécution automatique de l'action si le LLM retourne un JSON valide
        try:
            action_data = json.loads(response)
            do([action_data])
            print("Action exécutée !")
        except Exception as e:
            print(f"Erreur lors de l'exécution de l'action : {e}")

if __name__ == "__main__":
    main()