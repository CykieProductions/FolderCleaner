import os

class Helpers:
    def join_path_str(*paths:str) -> str:
        return os.path.join(*paths).replace("\\", "/")