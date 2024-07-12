import winshell
import pymsgbox

from datetime import date, timedelta
import os

from folder_cleaner.helpers import Helpers

trash_schedule_path = Helpers.join_path_str(Helpers.DATA_PATH, "trash schedule.txt")

def save_scheduled_date(scheduled_date:date, path:str) -> date:
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    
    with open(path, 'w') as file:
        file.write(scheduled_date.isoformat())

def load_scheduled_date(path:str) -> date:
    if not os.path.exists(path):
        scheduled_date = date.today()
        os.makedirs(os.path.dirname(path))
        save_scheduled_date(scheduled_date, path)
    else:
        with open(path, 'r') as file:
            date_str = file.read().strip()
            scheduled_date = date.fromisoformat(date_str)
            
    return scheduled_date

def is_scan_ready(scheduled_date:date) -> bool:
    if scheduled_date is None:
        scheduled_date = load_scheduled_date(trash_schedule_path)
    
    result = date.today() >= scheduled_date
    return result

async def try_empty_trash(max_size:int) -> bool:
    trash_size_mb = await Helpers.get_directory_size(Helpers.RECYCLE_PATH)
    
    if trash_size_mb >= max_size:
        choice = pymsgbox.confirm(
        f"This PC's Recycle Bin is taking up more than {max_size}MB (currently {trash_size_mb:.2f}MB)\n" +
        "Do you want to empty it?",
        "Empty the Recycle Bin?", (pymsgbox.OK_TEXT, pymsgbox.CANCEL_TEXT), _tkinter = False)
        
        if choice == pymsgbox.OK_TEXT:
            winshell.recycle_bin().empty()
            save_scheduled_date(date.today() + timedelta(weeks=3), trash_schedule_path)
            return True
        else:
            save_scheduled_date(date.today() + timedelta(days=2), trash_schedule_path)
        
    return False #REVIEW - Consider an enum instead of a bool