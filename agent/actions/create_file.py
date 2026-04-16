def create_file(file_name):
    import os
    file_path = "files/" + file_name
    os.makedirs("files", exist_ok=True)
    with open(file_path, 'w+'):
        pass
    print(f"[create_file] Created file at: {os.path.abspath(file_path)}")

