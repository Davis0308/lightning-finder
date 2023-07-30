# ruff: noqa: E501

class MainSettings:
    delete_proc_dir_when_done = True #choose whether to delete the processing folder once the script finishes [default: True]
    proc_dir_name = "processing" #choose name of processing dir [default: processing]
    video_file_name = "video.mp4" #name of the video file to process in the root folder [default: video.mp4]
    custom_frameres = False #choose if the frames should be rendered at the same resolution as they are in the video (False) or if you'd like to change frame resolution in frame_res (True) [default: False]
    frame_res = "1920x1080" # WidthxHeight [default: 1920x1080]
    average_brightness_algo = 2 #choose the brightness algorithm, from 0 to 6 (check functions.py) [default: 2]
