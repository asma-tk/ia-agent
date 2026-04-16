def writein_file(file_name, content):
    import os
    files_dir = os.path.join(os.path.dirname(__file__), '../../files')
    os.makedirs(files_dir, exist_ok=True)
    file_path = os.path.join(files_dir, file_name)
    with open(file_path, "w+") as file:
        file.write(content)