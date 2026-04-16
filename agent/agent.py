from actions.list_of_actions import LIST_OF_ACTIONS
import shutil

def do(actions_list: list[dict]):
    for call in actions_list:
        LIST_OF_ACTIONS[call["action"]](*call["params"])

# Simple example: create 'files' directory and copy files into it using shutil
import os



# Mi
# Example usage:
# download_files_to_new_dir(["example1.txt", "example2.txt"])


