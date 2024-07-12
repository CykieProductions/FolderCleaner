import math
import os
import re

class Helpers:
    
    @staticmethod
    def join_path_str(*paths:str) -> str:
        return os.path.join(*paths).replace("\\", "/")
    
    @staticmethod
    def add_numeric_suffix(full_file_name):
        # Split into name and extension
        base_name, ext = os.path.splitext(full_file_name)
        
        # Extract the existing numeric suffix (if any)
        pattern = re.search(r"_(\d+)$", base_name)
        if pattern:
            new_suffix = int(pattern.group(1)) + 1
            new_base_name = base_name[:pattern.start()]
        else:
            new_suffix = 2
            new_base_name = base_name
        
        # Construct the new file name
        new_file_name = f"{new_base_name}_{new_suffix}{ext}"
        return new_file_name
    
    
    def byte_to_mb(mb:int) -> int:
        return mb / (1024 * 1024)
    
    def mb_to_byte(bytes:int) -> int:
        return bytes * 1024 * 1024
    
    async def get_directory_size(directory:str, size_cap_mb:int = -1) -> int:
        if size_cap_mb == -1:
            size_cap_mb = math.inf
        
        total_size = 0
        for (dirpath, dirnames, filenames) in os.walk(directory):
            for file_name in filenames:
                file_path = Helpers.join_path_str(dirpath, file_name)
                total_size += os.path.getsize(file_path)
                
                # do we need to keep going?
                if total_size > Helpers.mb_to_byte(size_cap_mb):
                    return Helpers.byte_to_mb(total_size)
            
        return Helpers.byte_to_mb(total_size)
    
    
    RECYCLE_PATH = "C:/$Recycle.Bin"
    APP_NAME = "Cykie Folder Cleaner"
    DATA_PATH = join_path_str(os.getenv('LOCALAPPDATA'), "Cykie Productions", APP_NAME)
    USER_PATH = os.path.expanduser('~').replace("\\", "/")
    DOWNLOADS_PATH = join_path_str(USER_PATH, "Downloads")
    