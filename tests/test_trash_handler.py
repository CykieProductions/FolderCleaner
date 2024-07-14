import pymsgbox
import winshell
import pytest
from unittest.mock import patch, MagicMock

from folder_cleaner.trash_handler import *

@pytest.mark.parametrize('box_val,expected,max_size', 
                        [('OK', TrashCheckEnum.EMPTIED, 64), 
                        ('OK', TrashCheckEnum.NOT_FULL, 3000), 
                        ('Cancel', TrashCheckEnum.DENIED, 64)
                        ])
async def test_try_empty_trash(box_val, expected, max_size):
    with patch('pymsgbox.confirm') as mock_confirm, \
    patch('winshell.recycle_bin') as mock_recycle_bin:
        # Arrange
        mock_confirm.return_value = box_val
        mock_recycle_bin.return_value.empty = MagicMock()
        
        # Assume the size of the recycle bin is 2000MB
        with patch.object(Helpers, 'get_directory_size', return_value=2000) as mock_get_directory_size:
            # Act
            result = await try_empty_trash(max_size)    
        
        # Assert
        mock_get_directory_size.assert_called_once_with(Helpers.RECYCLE_PATH)
        
        if (max_size < 2000):
            mock_confirm.assert_called_once()
            
            if mock_confirm.return_value == 'OK':
                mock_recycle_bin.return_value.empty.assert_called_once() # emptied
            else:
                mock_recycle_bin.return_value.empty.assert_not_called()# not emptied
            
        assert result == expected