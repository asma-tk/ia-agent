def writein_file(file_name, content):
    import os
    file_path = "../files/" + file_name
    os.makedirs("files", exist_ok=True)
    with open(file_path, "w+") as file:
        file.write(content)