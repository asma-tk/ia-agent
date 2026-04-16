import os
import re

def execute_regex(file_name, pattern):
    """
    Supprime tous les caractères correspondant au pattern regex dans le fichier files/file_name.
    Si pattern == '{}', supprime toutes les accolades { et }.
    """
    file_path = os.path.join('files', file_name)
    with open(file_path, "r") as file:
        content = file.read()

    # Si le pattern demandé est '{}', on veut remplacer les accolades { et } par une chaîne vide
    if pattern == '{}':
        regex_pattern = r'[{}]'
    else:
        regex_pattern = pattern

    result = re.sub(regex_pattern, '', content)

    with open(file_path, "w") as file:
        file.write(result)
    print(f"Characters matching '{regex_pattern}' deleted from {file_name}.")