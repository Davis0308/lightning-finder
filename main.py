# ruff: noqa: E501
import cv2
import os
import subprocess
import time
import matplotlib.pyplot as plt
import shutil
#import math

import functions
import config

from pathlib import Path
#from PIL import Image
#from PIL import ImageStat


#starting timer to meter how long the process takes
timer_start = time.time()

#defining current working directory
cwd = Path.cwd()

#defining processing folder path
processing_dir_name = config.settings.proc_dir_name
processing_dir = cwd / processing_dir_name

#checking if processing folder doesn't exist; if it doesn't, create it
if os.path.exists(processing_dir) is False:
    os.mkdir(processing_dir)
    print("processing folder created\n")
else:
    print("processing folder already exists\n")

#checking if processing folder is empty; if not, ask to delete items
if len(os.listdir(processing_dir)) != 0:
    proc_empty_input = input("WARNING:\n"
    "The processing folder is not empty. "
    "To continue, the contents of the folder need to be deleted. "
    "Please check that you don't have any important files in the "
    "folder as they will be removed. "
    "Would you like to continue?\n(yes/No): ").lower()
    if proc_empty_input == "yes":
        functions.clear_dir_only_if_exists(processing_dir, processing_dir_name)
    else:
        exit()

#defining output file for ffmpeg
ffmpeg_output = f"{processing_dir}/%d.png"

#running ffmpeg command to split video in frames
subprocess.run(["ffmpeg","-i",config.settings.video_file_name,ffmpeg_output])

#getting video's FPS
fpsfind = cv2.VideoCapture("video.mp4")
fps = fpsfind.get(cv2.CAP_PROP_FPS)
fps = round(fps, 3)
print("\n\n\n" + "fps: " + str(fps))

#creating final array for brightness values
brightness_array = []

#counting number of frames in the folder processing and
#putting it in the variable frame_count
frame_count = 0
for path in os.scandir(processing_dir):
    if path.is_file():
        frame_count += 1
print("number of frames: " + str(frame_count))

#listing methods for easy switching while testing
bf1 = functions.get_average_perceived_brightness
bf2 = functions.get_average_grayscale_brightness
bf3 = functions.get_rms_perceived_brightness
bf4 = functions.get_rms_grayscale_brightness
bf5 = functions.get_average_equal_brightness

#making loop for extracting brightness of every frame
for frame_number in range(1, frame_count+1):
    frame_brightness = bf1(processing_dir_name, frame_number)
    brightness_array.append(frame_brightness)

#creating final array for timestamp values
timestamp_array = []

#making loop for calculating timestamp of every frame
for n in range(frame_count):
    timestamp_in_s = n/fps
    timestamp_in_s = round(timestamp_in_s, 3)
    timestamp_array.append(timestamp_in_s)

#creating plotted graph
print("\n\nbrightness data points: " + str(len(brightness_array)))
print("timestamp data points: " + str(len(timestamp_array)))
plt.plot(timestamp_array, brightness_array)

#deleting contents of processing folder
if config.settings.delete_proc_dir_when_done is True:
    nofipf = len(os.listdir(processing_dir)) #getting num. of files in processing folder
    shutil.rmtree(processing_dir)
    print(f"files removed in .\\{processing_dir_name}: {nofipf}")

#ending timer
timer_end = time.time()
time_elapsed = (timer_end-timer_start)
time_elapsed = round(time_elapsed, 2)
print("\n\nFinished." + "\nProcess took " + str(time_elapsed) + " seconds.")

#showing plot
plt.show()
