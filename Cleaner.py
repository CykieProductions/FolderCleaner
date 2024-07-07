from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import time
import json
import shutil

from file_group import FileGroup
from helpers import *

USER_PATH = os.path.expanduser('~').replace("\\", "/")

class FolderHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for fileName in os.listdir(tracked_Path):
            file_path = Helpers.join_path_str(tracked_Path, fileName)
            #skip if directory is found
            if os.path.isdir(file_path):
                continue
            
            for group in file_groups:
                destination = group.get_file_destination(fileName)
                if destination is not None:
                    os.rename(file_path, destination)
        

tracked_Path = Helpers.join_path_str(USER_PATH, "Downloads")

image_group = FileGroup(Helpers.join_path_str(USER_PATH, "Pictures", "Downloaded"), 
                        [".jpg", ".jpeg", ".png", ".gif", ".webp",])

video_group = FileGroup(Helpers.join_path_str(USER_PATH, "Video", "Downloaded"), 
                        [".mp4", ".mkv"])

audio_group = FileGroup(Helpers.join_path_str(USER_PATH, "Music", "Downloaded"), 
                        [".mp3", ".wav", ".ogg"])

file_groups = [image_group, video_group, audio_group,]


event_handler = FolderHandler()
observer = Observer()

observer.schedule(event_handler, tracked_Path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()

print("Goodnight")