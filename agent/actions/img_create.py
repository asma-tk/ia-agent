# Imports PIL module
from PIL import Image

# creating a image object (new image object) with
# RGB mode and size 200x200



# Pixel art smiley face generator
def img_create(image_name):
    import os
    img = Image.new("RGB", (8, 8), "black")
    pixels = img.load()
    # eyes
    pixels[2, 2] = (255, 255, 255) #(2,2) cest la position.  2 pixels a droite et 2 pixels en bas a partir du coin superieur gauche de l'image. (255,255,255) cest la couleur blanche en RGB
    pixels[5, 2] = (255, 255, 255)
    # mouth
    pixels[2, 5] = (255, 255, 255)
    pixels[3, 6] = (255, 255, 255)
    pixels[4, 6] = (255, 255, 255)
    pixels[5, 5] = (255, 255, 255)
    # scale up for visibility
    img = img.resize((200, 200), Image.NEAREST)
    # Ensure the files directory exists
    os.makedirs("../files", exist_ok=True)
    img.save(f"../files/{image_name}.png")
    img.show()

# Example usage:
if __name__ == "__main__":
    img_create()
