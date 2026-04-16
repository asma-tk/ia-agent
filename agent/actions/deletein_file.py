# i wannna delete a texxt in a file but i dont wanna delete the file itself
import os
def deletein_file(file_name, content):
    import os
    files_dir = os.path.join(os.path.dirname(__file__), '../../files')
    os.makedirs(files_dir, exist_ok=True)
    file_path = os.path.join(files_dir, file_name)
    with open(file_path, "r+") as f:
        f.seek(0)
        f.truncate()
    print("Cleared")