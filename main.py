# ruff: noqa: E501
import cv2
import os
#import subprocess
import time
import matplotlib.pyplot as plt
import shutil
#import math

import functions

from pathlib import Path
#from PIL import Image
#from PIL import ImageStat
from configparser import ConfigParser


#initializing configparser and defining config file
configini=ConfigParser(comment_prefixes='', allow_no_value=True)
configini.read('config.ini')

#starting timer to meter how long the process takes
timer_start_performance = time.perf_counter()
timer_start_process = time.process_time()

#Printing script info
print("lightning-finder by Davis0308 - github.com/Davis0308/lightning-finder - GNU GPL V3\n")

#defining current working directory
cwd = Path.cwd()
cwd_name = "lightning-finder"

#defining processing folder path
processing_dir_name = configini.get("MainSettings","proc_dir_name")
processing_dir = cwd / processing_dir_name

#defining video file name
video_file_name = configini.get("MainSettings","video_file_name")
print(f"Video to process: {video_file_name}")

#checking if processing folder doesn't exist; if it doesn't, create it
print("Checking for the existance of processing folder...")
if os.path.exists(processing_dir) is False:
    os.mkdir(processing_dir)
    print(f"Processing folder named {processing_dir_name} created.\n")
else:
    print("Processing folder already exists.\n")

#checking if processing folder is empty; if not, ask to delete items
if len(os.listdir(processing_dir)) != 0:
    print("\033[91mWARNING:\033[0m")
    proc_empty_input = input(f"The processing folder located at .\\{cwd_name}\\{processing_dir_name} is not empty.\n"
    "To continue, the contents of the folder need to be deleted.\n"
    "Please check that you don't have any important files in the "
    "folder as they will be removed.\n"
    "Would you like to continue?\n(yes/No): ").lower()
    if proc_empty_input == "yes":
        functions.clear_dir_only_if_exists(processing_dir, processing_dir_name, cwd_name)
    else:
        exit()

#defining output file for ffmpeg
ffmpeg_output = f"{processing_dir}/%d.png"

#running ffmpeg command to split video in frames
if configini.getboolean("MainSettings","custom_frameres") is True:
    functions.ffmpeg_custom_frameres(ffmpeg_output, video_file_name, configini.get("MainSettings","frame_res"))
else:
    functions.ffmpeg_normal(ffmpeg_output, video_file_name)


#getting video's FPS
fpsfind = cv2.VideoCapture(video_file_name)
fps = fpsfind.get(cv2.CAP_PROP_FPS)
fps = round(fps, 3)
print(f"\nFps: {fps}")

#creating final array for brightness values
brightness_array = []

#counting number of frames in the folder processing and
#putting it in the variable frame_count
frame_count = 0
for path in os.scandir(processing_dir):
    if path.is_file():
        frame_count += 1
print(f"Number of frames: {frame_count}")


#making loop for extracting brightness of every frame
average_brightness_algorithm = configini.getint("MainSettings","average_brightness_algorithm")
print(f"Processing data with algorithm n. {average_brightness_algorithm}...")
for frame_number in range(1, frame_count+1):
    frame_brightness = functions.brightness_tuple[average_brightness_algorithm](processing_dir_name, frame_number)
    brightness_array.append(frame_brightness)

#creating final array for timestamp values
timestamp_array = []
timestamp_array_noms = []

#making loop for calculating timestamp of every frame both in seconds and milliseconds
try:
    for n in range(frame_count):
        timestamp_in_s = n/fps
        timestamp_in_s = round(timestamp_in_s, 3)
        timestamp_in_ms = timestamp_in_s * 1000
        ms_to_hhmmssmsmsms = functions.ms_to_hh_mm_ss_msmsms(timestamp_in_ms)
        s_to_hhmmss = functions.s_to_hh_mm_ss(timestamp_in_s)
        timestamp_array.append(ms_to_hhmmssmsmsms)
        timestamp_array_noms.append(s_to_hhmmss)
except ZeroDivisionError as zerodiv_error:
    print(f"ERROR: {zerodiv_error}")
    exit()

#creating plotted graph
print(f"\nBrightness data points acquired: {len(brightness_array)}")
print(f"Timestamp data points acquired: {len(timestamp_array)}")
plot = plt.plot(timestamp_array, brightness_array)
plt.xticks(rotation=45)
plt.title("Video brightness over time")
plt.xlabel(xlabel="Timestamp", labelpad=5)
plt.ylabel(ylabel="Brightness", labelpad=10)

# Calculate the number of desired tick labels
desired_num_ticks = configini.getint("MainSettings","number_of_labels_in_plot")
# Calculate the step size for ticks
try:
    step = len(timestamp_array) // desired_num_ticks
except ZeroDivisionError as zerodiv_error:
    print(f"ERROR: {zerodiv_error}")
    exit()
# Set custom x-axis ticks
plt.xticks(timestamp_array[::step])

#deleting contents of processing folder
if configini.getboolean("MainSettings","delete_proc_dir_when_done") is True:
    number_of_files_in_processing_folder = len(os.listdir(processing_dir)) #getting num. of files in processing folder
    shutil.rmtree(processing_dir)
    print(f"{number_of_files_in_processing_folder} files removed in .\\{cwd_name}\\{processing_dir_name}")

#ending timers
timer_end_performance = time.perf_counter()
time_elapsed_performance = (timer_end_performance-timer_start_performance)
time_elapsed_performance = round(time_elapsed_performance, 2)
print(f"\n\nFinished.\nScript execution took {time_elapsed_performance} seconds")

timer_end_process = time.process_time()
time_elapsed_process = (timer_end_process-timer_start_process)
time_elapsed_process = round(time_elapsed_process, 2)
print(f"Process took {time_elapsed_process} seconds\n")

#showing plot
plt.show()
