import os

class Helpers:
    def join_path_str(*names:str) -> str:
        return os.path.join(names).replace("\\", "/")