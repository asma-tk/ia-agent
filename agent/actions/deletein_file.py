# i wannna delete a texxt in a file but i dont wanna delete the file itself
import os
def deletein_file(file_name, content):
    with open(file_name, "r+") as f:
     f.seek(0) # Move the cursor to the beginning of the file
     f.truncate()

     print("Cleared")
pass