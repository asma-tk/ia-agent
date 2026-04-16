import os


def delete_file(file_name):
    import os
    files_dir = os.path.join(os.path.dirname(__file__), '../../files')
    file_path = os.path.join(files_dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The file does not exist")