from unittest.mock import patch
import pytest
import os

from folder_cleaner import file_group
from folder_cleaner.helpers import Helpers


@pytest.mark.parametrize("test_input,expected", 
                            [("video.mkv", Helpers.join_path_str(file_group.video_group.target_path, "video.mkv")), 
                            ("fail.jpeg", None),
                            ("movie.mp4", Helpers.join_path_str(file_group.video_group.target_path, "movie.mp4")
                            )])
def test_get_file_destination(test_input, expected):
    
    with patch.object(os, "makedirs") as mock_makedirs:
        result = file_group.video_group.get_file_destination(test_input)
        print(f"os.makedirs was called with: {mock_makedirs.call_args}")
    
    assert result == expected