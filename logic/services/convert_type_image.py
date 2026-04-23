from PIL import Image

def convert_image(input_path, output_path, output_format):
    image = Image.open(input_path)

image = Image.open("database/images/BMWX7.jfif")
image.save("database/images/BMWX7.png", "PNG")