# ruff: noqa: E501
import os
import shutil
from PIL import Image
from PIL import ImageStat
import math
import subprocess

#remove files from a folder only if the folder exists
def clear_dir_only_if_exists(directory_to_remove, directory_name, current_directory):
    if os.path.exists(directory_to_remove) is True:
        print("Deleting...")
        shutil.rmtree(directory_to_remove)
        os.mkdir(directory_to_remove)
        print(f"Contents of the folder .\\{current_directory}\\{directory_name} deleted successfully.\n")
    else:
        print(f"The folder .\\{current_directory}\\{directory_name} does not exist anymore. "
              "Creating it and continuing.\n")
        os.mkdir(directory_to_remove)


##brightness extraction algorithm functions

#0) original, RGB
#Average pixels, then transform to "perceived brightness"
def get_average_perceived_brightness(processing_dir_name, frame_number):
    im = Image.open(f"{processing_dir_name}/{frame_number}.png")
    r, g, b = ImageStat.Stat(im).mean
    brightness = (math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)))
    return(brightness)

#1)
#Convert image to grayscale, return average pixel brightness
def get_average_grayscale_brightness(processing_dir_name, frame_number):
   im = Image.open(f"{processing_dir_name}/{frame_number}.png").convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]

#2) (one of the better ones)
#RMS of pixels, then transform to "perceived brightness"
def get_rms_perceived_brightness(processing_dir_name, frame_number):
   im = Image.open(f"{processing_dir_name}/{frame_number}.png")
   stat = ImageStat.Stat(im)
   r,g,b = stat.rms
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

#3)
#Convert image to greyscale, return RMS pixel brightness.
def get_rms_grayscale_brightness(processing_dir_name, frame_number):
   im = Image.open(f"{processing_dir_name}/{frame_number}.png").convert('L')
   stat = ImageStat.Stat(im)
   return stat.rms[0]

#4)
#Average pixels, then transform to equal brightness
def get_average_equal_brightness(processing_dir_name, frame_number):
    im = Image.open(f"{processing_dir_name}/{frame_number}.png")
    r, g, b = ImageStat.Stat(im).mean
    brightness = (math.sqrt((r**2) + (g**2) + (b**2)))
    return(brightness)

#5)
#Average pixels, then transform to "perceived brightness" but with blue prevalence
def get_average_perceived_blue_brightness(processing_dir_name, frame_number):
    im = Image.open(f"{processing_dir_name}/{frame_number}.png")
    r, g, b = ImageStat.Stat(im).mean
    brightness = (math.sqrt(0.241*(r**2) + 0.1*(g**2) + 0.691*(b**2)))
    return(brightness)

#6)
#Random for testing
def get_random_test_brightness(processing_dir_name, frame_number):
    im = Image.open(f"{processing_dir_name}/{frame_number}.png")
    r, g, b = ImageStat.Stat(im).average
    brightness = (math.log2(math.sqrt(0.241*(r**5) + 0.1*(g**5)) + 0.391*(b**3)))
    return(brightness)

#declaring function variables
brightness_function_0 = get_average_perceived_brightness
brightness_function_1 = get_average_grayscale_brightness
brightness_function_2 = get_rms_perceived_brightness
brightness_function_3 = get_rms_grayscale_brightness
brightness_function_4 = get_average_equal_brightness
brightness_function_5 = get_average_perceived_blue_brightness
brightness_function_6 = get_random_test_brightness
brightness_tuple = (brightness_function_0, brightness_function_1,
                    brightness_function_2, brightness_function_3,
                    brightness_function_4, brightness_function_5,
                    brightness_function_6)


#different ffmpeg modes

#normal
def ffmpeg_normal(ffmpeg_output, video_file_name):
    subprocess.run(["ffmpeg", "-i", video_file_name, ffmpeg_output])

#with custom frame resolution
def ffmpeg_custom_frameres(ffmpeg_output, video_file_name, custom_resolution):
    subprocess.run(["ffmpeg", "-i", video_file_name, "-s", custom_resolution, ffmpeg_output])
