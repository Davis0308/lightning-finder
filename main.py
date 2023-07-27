import cv2
import os
import subprocess
import math
import time
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageStat
from pathlib import Path
import functions


#starting timer to meter how long the process takes
timer_start = time.time()

#defining current working directory
cwd = Path.cwd()

#defining output file for ffmpeg
ffmpeg_output = cwd / "processing/%d.png"

#defining processing folder path
processing_dir = cwd / "processing"

#running ffmpeg command to split video in frames
subprocess.run(["ffmpeg","-i","video.mp4",ffmpeg_output])

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

#making loop for extracting brightness of every frame
for frame_number in range(1, frame_count+1):
    im = Image.open(f"processing/{frame_number}.png")
    r, g, b = ImageStat.Stat(im).mean
    frame_brightness = 100*(math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)))
    frame_brightness = round(frame_brightness)
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

#ending timer
timer_end = time.time()
time_elapsed = (timer_end-timer_start)
time_elapsed = round(time_elapsed, 2)
print("\n\nFinished." + "\nProcess took " + str(time_elapsed) + " seconds.")

#showing plot
plt.show()