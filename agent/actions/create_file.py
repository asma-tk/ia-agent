def create_file(file_name):
    import os
    file_path = "../files/" + file_name
    try:
        os.makedirs("../files", exist_ok=True)
        with open(file_path, 'w+') as f:
            f.write("Ceci est un fichier créé automatiquement.\n")
        print(f"[create_file] Created file at: {os.path.abspath(file_path)}")
    except Exception as e:
        print(f"[create_file] ERROR: {e} (file_path={file_path})")

