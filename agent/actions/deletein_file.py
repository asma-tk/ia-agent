# i wannna delete a texxt in a file but i dont wanna delete the file itself
import os
def deletein_file(file_name, content):
    file_path = "../files/" + file_name
    os.makedirs("../files", exist_ok=True)
    with open(file_path, "r+") as f:
        f.seek(0)  # Move the cursor to the beginning of the file
        f.truncate() # Clear the file content
    print("Cleared")