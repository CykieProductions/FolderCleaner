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
    
    USER_PATH = os.path.expanduser('~').replace("\\", "/")
    DOWNLOADS_PATH = join_path_str(USER_PATH, "Downloads")