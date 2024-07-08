from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import time

from file_group import FileGroup
from helpers import *

USER_PATH = os.path.expanduser('~').replace("\\", "/")

class FolderHandler(FileSystemEventHandler):
    def on_modified(self, event):
        FolderHandler.update_folder(tracked_Path)
        
    def update_folder(path:str) -> None:
        for fileName in os.listdir(path):
            file_path = Helpers.join_path_str(tracked_Path, fileName)
            #skip if directory is found
            if os.path.isdir(file_path):
                continue
            
            for group in file_groups:
                destination = group.get_file_destination(fileName)
                
                #TODO add renaming logic for duplicate file names
                
                if destination is not None:
                    os.rename(file_path, destination)

#* File Tracking Info
tracked_Path = Helpers.join_path_str(USER_PATH, "Downloads")

image_group = FileGroup(Helpers.join_path_str(USER_PATH, "Pictures", "Downloaded"), 
                        [".jpg", ".jpeg", ".png", ".gif", ".webp",])

video_group = FileGroup(Helpers.join_path_str(USER_PATH, "Video", "Downloaded"), 
                        [".mp4", ".mkv"])

audio_group = FileGroup(Helpers.join_path_str(USER_PATH, "Music", "Downloaded"), 
                        [".mp3", ".wav", ".ogg"])

file_groups = [image_group, video_group, audio_group,]


#* Folder Watch Logic
event_handler = FolderHandler()
observer = Observer()

observer.schedule(event_handler, tracked_Path, recursive=True)
observer.start()
# manually look at the target folder to start
FolderHandler.update_folder(tracked_Path)

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()