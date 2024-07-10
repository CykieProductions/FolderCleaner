from unittest.mock import patch
import pytest

from folder_cleaner.file_group import *
from folder_cleaner.helpers import Helpers


@pytest.mark.parametrize("test_input,expected", 
                            [("video.mkv", Helpers.join_path_str(video_group.target_path, "video.mkv")), 
                            ("fail.jpeg", None),
                            ("movie.mp4", Helpers.join_path_str(video_group.target_path, "movie.mp4")
                            )])
def test_get_file_destination(test_input, expected):
    
    with patch.object(os, "makedirs") as mock_makedirs:
        result = video_group.get_file_destination(test_input)
        print(f"os.makedirs was called with: {mock_makedirs.call_args}")
    
    assert result == expected