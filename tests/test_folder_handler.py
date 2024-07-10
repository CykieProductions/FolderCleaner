import asyncio
import os
from unittest.mock import patch
import pytest

from source.file_group import *
from source.helpers import Helpers
from source.folder_handler import FolderHandler 

def test_update_folder():
    with patch.object(os, "rename") as mock_rename:
        with patch.object(os, "listdir", return_value=['video.mkv', 'audio.wav', 'image.jpeg']) as mock_listdir:
            handler = FolderHandler(Helpers.DOWNLOADS_PATH, file_groups) 
            asyncio.run(handler.update_folder_async())
        
    print(f"os.listdir was called with: {mock_listdir.call_args}") 
    print(f"os.rename was called with: {mock_rename.call_args}")
    
    #TODO Test with video and audio
    mock_rename.assert_called_with(Helpers.join_path_str(handler.tracked_path, 'image.jpeg'), 
                                    Helpers.join_path_str(handler.tracked_path, image_group.get_file_destination('image.jpeg')))


async def test_get_new_file_path():
    user = os.path.expanduser('~').replace("\\", "/")
    audio = FileGroup(Helpers.join_path_str(user, "Music", "Downloaded"), 
                        [".mp3", ".wav", ".ogg"])
    handler = FolderHandler(Helpers.DOWNLOADS_PATH, file_groups)
    
    result = await handler.get_new_file_path_async("fish.ogg", audio)
    
    assert result == Helpers.join_path_str(user, "Music", "Downloaded", "fish.ogg")
    
