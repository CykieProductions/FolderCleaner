#region Imports
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import time

from file_group import FileGroup
from helpers import *
#endregion

USER_PATH = os.path.expanduser('~').replace("\\", "/")

class FolderHandler(FileSystemEventHandler):
    
    def __init__(self, tracked_path:str = None):
        if tracked_path is None:
            tracked_path = Helpers.join_path_str(USER_PATH, "Downloads")
        self.tracked_path = tracked_path
    
    def on_modified(self, event):
        FolderHandler.update_folder(self.tracked_path)
    
    def update_folder(self, path:str = None) -> None:
        if path is None:
            path = self.tracked_path
            
        for full_file_name in os.listdir(path):
            for group in file_groups:
                destination = FolderHandler.get_new_file_path(full_file_name, group)
                
                if destination:
                    os.rename(Helpers.join_path_str(path, full_file_name), destination)
    
    @staticmethod
    def get_new_file_path(self, full_file_name:str, group:FileGroup) -> str:
        file_path = Helpers.join_path_str(self.tracked_path, full_file_name)
        
        #skip if directory is found
        if os.path.isdir(file_path):
            return None
        
        destination = group.get_file_destination(full_file_name)
        
        #TODO add renaming logic for duplicate file names
        if os.path.exists(destination):
            new_file_name = Helpers.add_numeric_suffix(full_file_name)
            destination = os.path.join(os.path.dirname(file_path), new_file_name)
            return destination
#end of FolderHandler

#* File Tracking Info

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

observer.schedule(event_handler, event_handler.tracked_path, recursive=True)
observer.start()
# manually look at the target folder to start
event_handler.update_folder()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()