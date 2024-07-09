from watchdog.events import FileSystemEventHandler

import os

from file_group import FileGroup
from helpers import *


class FolderHandler(FileSystemEventHandler):
    
    def __init__(self, tracked_path:str, file_groups:FileGroup):
        self.tracked_path = tracked_path
        self.file_groups = file_groups
    
    def on_modified(self, event):
        self.update_folder(self.tracked_path)
    
    def update_folder(self, path:str = None) -> None:
        if not path:
            path = self.tracked_path
        
        dir = os.listdir(path)
        for full_file_name in dir:
            for group in self.file_groups:
                destination = self.get_new_file_path(full_file_name, group)
                
                if destination:
                    os.rename(Helpers.join_path_str(path, full_file_name), destination)
    
    def get_new_file_path(self, full_file_name:str, group:FileGroup) -> str:
        old_file_path = Helpers.join_path_str(self.tracked_path, full_file_name)
        
        #skip if directory is found
        if os.path.isdir(old_file_path):
            return None
        
        destination = group.get_file_destination(full_file_name)
        new_file_name = full_file_name
        
        i = 0
        while destination and os.path.exists(destination):
            if i > 99: break
            new_file_name = Helpers.add_numeric_suffix(new_file_name)
            destination = Helpers.join_path_str(group.target_path, new_file_name)
            i += 1
        return destination