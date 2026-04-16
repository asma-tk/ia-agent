def create_file(file_name):
    import os
    files_dir = os.path.join(os.path.dirname(__file__), '../../files')
    os.makedirs(files_dir, exist_ok=True)
    file_path = os.path.join(files_dir, file_name)
    with open(file_path, 'w+'):
        pass
    print(f"[create_file] Created file at: {os.path.abspath(file_path)}")

