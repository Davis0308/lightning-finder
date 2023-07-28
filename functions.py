import os
import shutil
from PIL import Image
from PIL import ImageStat
import math

#remove files from a folder only if the folder exists
def clear_dir_only_if_exists(directory_to_remove, directory_name):
    if os.path.exists(directory_to_remove) is True:
        shutil.rmtree(directory_to_remove)
        os.mkdir(directory_to_remove)
        print(f"contents of the folder .\\{directory_name} deleted successfully\n")
    else:
        print(f"the folder .\\{directory_name} does not exist anymore. "
              "Creating it and continuing.\n")
        os.mkdir(directory_to_remove)


##brightness extraction functions

#1) original, RGB
#Average pixels, then transform to "perceived brightness"
def get_average_perceived_brightness(processing_dir_name, frame_number):
    im = Image.open(f"{processing_dir_name}/{frame_number}.png")
    r, g, b = ImageStat.Stat(im).mean
    brightness = (math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)))
    brightness = round(brightness)
    return(brightness)

#2)
#Convert image to grayscale, return average pixel brightness
def get_average_grayscale_brightness(processing_dir_name, frame_number):
   im = Image.open(f"{processing_dir_name}/{frame_number}.png").convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]

#3)
#RMS of pixels, then transform to "perceived brightness"
def get_rms_perceived_brightness(processing_dir_name, frame_number):
   im = Image.open(f"{processing_dir_name}/{frame_number}.png")
   stat = ImageStat.Stat(im)
   r,g,b = stat.rms
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

#4)
#Convert image to greyscale, return RMS pixel brightness.
def get_rms_grayscale_brightness(processing_dir_name, frame_number):
   im = Image.open(f"{processing_dir_name}/{frame_number}.png").convert('L')
   stat = ImageStat.Stat(im)
   return stat.rms[0]

#5)
#Average pixels, then transform to equal brightness
def get_average_equal_brightness(processing_dir_name, frame_number):
    im = Image.open(f"{processing_dir_name}/{frame_number}.png")
    r, g, b = ImageStat.Stat(im).mean
    brightness = (math.sqrt((r**2) + (g**2) + (b**2)))
    brightness = round(brightness)
    return(brightness)
