import os

from helpers import Helpers

def test_join_path_str():
    assert Helpers.join_path_str(os.path.expanduser('~'), "this", "should", "work.txt") == \
        f"{os.path.expanduser('~').replace("\\", "/")}/this/should/work.txt"
    assert Helpers.join_path_str("c\\:TestUser", "not", "real.mp3") == \
        f"c/:TestUser/not/real.mp3"

def test_add_numeric_suffix():
    assert Helpers.add_numeric_suffix("e.png") == "e_2.png"
    assert Helpers.add_numeric_suffix("test_2.png") == "test_3.png"