import sys
sys.path.append(".")

from watchdog.observers import Observer

import asyncio
from datetime import date

from folder_handler import FolderHandler
from file_group import *
from helpers import *
import trash_handler



#* Folder Watch Logic
async def run_observer():
    downloads_handler = FolderHandler(Helpers.join_path_str(Helpers.USER_PATH, "Downloads"), file_groups)
    downloads_observer = Observer()
    
    downloads_observer.schedule(downloads_handler, downloads_handler.tracked_path, recursive=False)
    downloads_observer.start()
    # manually check the target folder to start
    await downloads_handler.update_folder_async()
    
    #* Init Trash Check
    scheduled_trash_date:date
    empty_trash_task:asyncio.Task
    
    async def load_trash_schedule_async(delay:float = 0):
        nonlocal scheduled_trash_date
        
        if delay > 0:
            await asyncio.sleep(delay)
        
        scheduled_trash_date = trash_handler.load_scheduled_date(trash_handler.trash_schedule_path)
    
    def update_trash_schedule_callback(future):
        nonlocal scheduled_trash_date
        print('Trash was checked. is_too_full:', future.result())
        if future.result():
            load_trash_schedule_async()# immediately load the schedule cause it likely changed
        else:#REVIEW - a bool may be too simple. However, I haven't seen serious side effects of this being called after a "cancel" in addition to the intended "failure"
            delay = 15
            asyncio.create_task(load_trash_schedule_async(delay))# check the schedule again soon
            print(f"Checking again in {delay} seconds.")
        print('Next scheduled trash date:', scheduled_trash_date, '\n')
    
    def run_trash_check():
        nonlocal scheduled_trash_date, empty_trash_task
        
        if trash_handler.is_scan_ready(scheduled_trash_date):
            scheduled_trash_date = date.max
            empty_trash_task = asyncio.create_task(trash_handler.try_empty_trash(90))
            empty_trash_task.add_done_callback(update_trash_schedule_callback)
        else:
            print("Trash is not scheduled to be checked until:", scheduled_trash_date)
    
    await load_trash_schedule_async()
    
    run_trash_check()
    
    try:
        while True:
            #time.sleep(10)
            await asyncio.sleep(10)
            
            if empty_trash_task is not None and empty_trash_task.done():
                run_trash_check()
            
    except KeyboardInterrupt:
        downloads_observer.stop()
        empty_trash_task.cancel()
    
    downloads_observer.join()

## MAIN ##
def main():
    asyncio.run(run_observer())

#! Guard against outside calls (ex: tests)
if __name__ == "__main__":
    main()