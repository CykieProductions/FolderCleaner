import pytest

from helpers import Helpers
from file_group import *


@pytest.mark.parametrize("test_input,expected", 
                            [("video.mkv", Helpers.join_path_str(video_group.target_path, "video.mkv")), 
                            ("fail.ogg", None),
                            ("movie.mp4", Helpers.join_path_str(video_group.target_path, "movie.mp4")
                            )])
def test_get_file_destination(test_input, expected):
    result = video_group.get_file_destination(test_input)
    
    assert result == expected