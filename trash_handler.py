from file_group import Helpers
from helpers import Helpers


import pymsgbox
import winshell


async def try_empty_trash(max_size:int = 2000) -> bool:
    trash_size_mb = await Helpers.get_directory_size(Helpers.RECYCLE_PATH)
    SNOOZE_TEXT = "Snooze"

    if trash_size_mb >= max_size:
        choice = pymsgbox.confirm(
        f"This PC's Recycle Bin is taking up more than {max_size}MB (currently {trash_size_mb:.2f}MB)\n" +
        "Do you want to empty it?",
        "Empty the Recycle Bin?", (pymsgbox.OK_TEXT, SNOOZE_TEXT, pymsgbox.CANCEL_TEXT), _tkinter = False)

        if choice == pymsgbox.OK_TEXT:
            winshell.recycle_bin().empty()
            return True
        elif choice == SNOOZE_TEXT:
            #TODO - Implement snooze
            pass
    return False