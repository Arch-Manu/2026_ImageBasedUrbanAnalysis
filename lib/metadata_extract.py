from PIL import Image, ImageStat
from PIL.ExifTags import IFD, TAGS
from pathlib import Path
import os

#Path to the root directory and image directory

ROOT_DIR = Path(__file__).parent.parent
IMG_DIR = ROOT_DIR / "images"


#collect images

images = []

for file in os.listdir(IMG_DIR):
    if file.endswith(('.JPG', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
        images.append(os.path.join(IMG_DIR, file))



#main definition

def extractmetadata(image_path):

    img_name = Path(image_path).name
    print("\nExtracting metadata from:", img_name)

    #Open image

    image = Image.open(image_path)
    exif_data = image.getexif()
    
    
    all_metadata = {}

    for k, v in exif_data.items():
        all_metadata[TAGS.get(k)] =  v
      
    keys = ("DateTime", "YResolution", "XResolution")
    return {k: all_metadata.get(k) for k in keys}



def extract_pixel_info(image_path):
        pixel_info = {}
        
        image = Image.open(image_path)
        stats = ImageStat.Stat(image)


        pixel_info["Total pixels"] = stats.count
        pixel_info["MinMax values"] = stats.extrema
        pixel_info["Mean Value"] = stats.mean
        pixel_info["Median Value"] = stats.median
        pixel_info["Variance"] = stats.var

        return pixel_info
   



if __name__ == "__main__":
    for image in images:
        print(extractmetadata(image))
        print(extract_pixel_info(image))

