import asyncio
import math
from watchdog.events import FileSystemEventHandler

import os

from .file_group import FileGroup
from .helpers import *


class FolderHandler(FileSystemEventHandler):
    
    def __init__(self, tracked_path:str, file_groups:FileGroup):
        self.tracked_path = tracked_path
        self.file_groups = file_groups
    
    def on_modified(self, event):
        asyncio.run(self.update_folder_async(self.tracked_path))
    
    async def update_folder_async(self, path:str = None) -> None:
        if not path:
            path = self.tracked_path
        
        dir = os.listdir(path)
        for full_file_name in dir:
            for group in self.file_groups:
                destination = await self.get_new_file_path_async(full_file_name, group)
                
                if destination:
                    os.rename(Helpers.join_path_str(path, full_file_name), destination)
    
    async def get_new_file_path_async(self, full_file_name:str, group:FileGroup) -> str:
        old_file_path = Helpers.join_path_str(self.tracked_path, full_file_name)
        
        #skip if directory is found
        if os.path.isdir(old_file_path):
            return None
        
        destination = group.get_file_destination(full_file_name)
        if not destination: 
            return None
        
        async def handle_suffix_async(dest, file_name, max_iterations:int = 100) -> str:
            i = 0
            if max_iterations < 0 or max_iterations is None:
                max_iterations = math.inf
            
            #REVIEW - Consider using asyncio timeout: https://docs.python.org/3/library/asyncio-task.html#id11
            while dest and os.path.exists(dest):
                if i >= max_iterations: break
                file_name = Helpers.add_numeric_suffix(file_name)
                dest = Helpers.join_path_str(group.target_path, file_name)
                i += 1
            return dest
        
        destination = await handle_suffix_async(destination, full_file_name, 100)
        
        return destination