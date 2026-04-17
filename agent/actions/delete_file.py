import os


def delete_file(file_name):
    import os
    file_path = "../files/" + file_name
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The file does not exist")