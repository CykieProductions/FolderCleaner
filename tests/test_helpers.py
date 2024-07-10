import os
import tempfile

import pytest

from folder_cleaner.helpers import Helpers

def test_join_path_str():
    assert Helpers.join_path_str(os.path.expanduser('~'), "this", "should", "work.txt") == \
        f"{os.path.expanduser('~').replace("\\", "/")}/this/should/work.txt"
    assert Helpers.join_path_str("c\\:TestUser", "not", "real.mp3") == \
        f"c/:TestUser/not/real.mp3"

def test_add_numeric_suffix():
    assert Helpers.add_numeric_suffix("e.png") == "e_2.png"
    assert Helpers.add_numeric_suffix("test_2.png") == "test_3.png"

@pytest.mark.parametrize("test_input,expected", [
                        (1000000, 0.953674),
                        (2097152, 2),
                        ])
def test_byte_to_mb(test_input, expected):
    result = Helpers.byte_to_mb(test_input)
    assert f"{result:.6f}" == f"{expected:.6f}"

@pytest.mark.parametrize("test_input,expected", [
                        (0.95367431640625, 1000000),
                        (2, 2097152),
                        ])
def test_mb_to_byte(test_input, expected):
    result = Helpers.mb_to_byte(test_input)
    assert f"{result:.6f}" == f"{expected:.6f}"
    
@pytest.fixture
def test_dir():
    # Create a temporary directory for testing
    dir = tempfile.TemporaryDirectory()
    yield dir
    # Clean up the temporary directory
    dir.cleanup()

async def test_get_directory_size(test_dir):
    # Create a test file in the temporary directory
    for i in range(3):
        test_file_path = os.path.join(test_dir.name, 'test_file' + str(i + 1))
        with open(test_file_path, 'w') as file:
            file.write('Hello, World!')
        
        # Test the get_directory_size function
        size = await Helpers.get_directory_size(test_dir.name)
        mb = Helpers.byte_to_mb(13 * (i + 1)) # size of 'Hello, World!'
        assert size == mb 