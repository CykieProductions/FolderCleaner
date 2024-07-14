import sys
sys.path.append(".")

from watchdog.observers import Observer
import asyncio

from folder_handler import FolderHandler
from file_group import *
from helpers import *
from trash_handler import load_trash_schedule_async, run_trash_check, empty_trash_task, load_trash_schedule_task



#* Folder Watch Logic
async def run_observer():
    global empty_trash_task, load_trash_schedule_task
    
    downloads_handler = FolderHandler(Helpers.join_path_str(Helpers.USER_PATH, "Downloads"), file_groups)
    downloads_observer = Observer()
    
    downloads_observer.schedule(downloads_handler, downloads_handler.tracked_path, recursive=False)
    downloads_observer.start()
    # manually check the target folder to start
    await downloads_handler.update_folder_async()
    
    # immediately check if you should do a full trash scan
    await load_trash_schedule_async()
    run_trash_check()
    
    try:
        while True:
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                raise KeyboardInterrupt
            
            # If you're not currently emptying the trash, attempt to empty it
            if empty_trash_task is None or empty_trash_task.done():
                run_trash_check()
            
    except KeyboardInterrupt:
        downloads_observer.stop()
        if empty_trash_task is not None:
            empty_trash_task.cancel()
            try:
                await empty_trash_task
            except asyncio.CancelledError:
                pass
        
        if load_trash_schedule_task is not None:
            load_trash_schedule_task.cancel()
            try:
                await load_trash_schedule_task
            except asyncio.CancelledError:
                pass
    
    
    downloads_observer.join()


## MAIN ##
def main():
    asyncio.run(run_observer())
    
    print("exiting...")

#! Guard against outside calls (ex: tests)
if __name__ == "__main__":
    main()