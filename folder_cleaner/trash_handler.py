import asyncio
import winshell
import pymsgbox

from datetime import datetime, date, time, timedelta 
import os

from folder_cleaner.helpers import Helpers


from enum import Enum

class TrashCheckEnum(Enum):
    NOT_FULL = 0
    EMPTIED = 1
    DENIED = 2

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
            return TrashCheckEnum.EMPTIED
        else:
            save_scheduled_date(date.today() + timedelta(days=2), trash_schedule_path)
            return TrashCheckEnum.DENIED
    
    save_scheduled_date(date.today() + timedelta(days=1), trash_schedule_path)
    return TrashCheckEnum.NOT_FULL

def alert_bedtime(bedtime:datetime):
    if datetime.now() > bedtime:
        pymsgbox.confirm("It's late, are you sure you want to continue?", "Bedtime")

#region #* Init Trash Check
scheduled_trash_date:date
empty_trash_task:asyncio.Task = None
load_trash_schedule_task:asyncio.Task = None

async def load_trash_schedule_async(delay:float = 0):
    global scheduled_trash_date
    
    if delay > 0:
        try:
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            raise
    
    scheduled_trash_date = load_scheduled_date(trash_schedule_path)
    print('Next scheduled trash date:', scheduled_trash_date, '\n')

def update_trash_schedule_callback(future):
    global scheduled_trash_date, load_trash_schedule_task
    
    print('Is the trash too full?', future.result() if future is not None else "Not checked")
    if future is not None and future.result() is not TrashCheckEnum.DENIED:
        asyncio.create_task(load_trash_schedule_async())# immediately load the schedule cause it likely changed
    else:
        delay = 60
        if (load_trash_schedule_task is None or load_trash_schedule_task.done()):
            load_trash_schedule_task = asyncio.create_task(load_trash_schedule_async(delay))# check the schedule again soon
            print(f"Reloading the schedule in {delay} seconds.\n")

def run_trash_check():
    global scheduled_trash_date, empty_trash_task
    
    if is_scan_ready(scheduled_trash_date):
        scheduled_trash_date = date.max
        empty_trash_task = asyncio.create_task(try_empty_trash(90))
        empty_trash_task.add_done_callback(update_trash_schedule_callback)
    else:
        update_trash_schedule_callback(None)# Periodically check the schedule for manual changes

#endregion
