import pytest
import os

import Cleaner as Cleaner
from file_group import FileGroup


def test_get_new_file_path():
    DEFAULT_HANDLER = Cleaner.FolderHandler()
    file_name = "python-test.ogg"
    
    result = DEFAULT_HANDLER.get_new_file_path(file_name, Cleaner.audio_group)
    assert os.path.dirname(result) == os.path.dirname()