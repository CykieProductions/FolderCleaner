import os
from helpers import *

class FileGroup:
    def __init__(self, path:str, extensions:list) -> None:    
        self.target_path = path
        self.valid_extensions = extensions
        
    def get_file_destination(self, file_name:str) -> str:
        for ext in self.valid_extensions:
            if file_name.endswith(ext):
                
                if not os.path.exists(self.target_path):
                    os.makedirs(self.target_path)
                
                return Helpers.join_path_str(self.target_path, file_name)
        return None