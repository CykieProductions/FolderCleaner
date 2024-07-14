import sys
sys.path.append(".")

from watchdog.observers import Observer

import asyncio
from datetime import date

from folder_handler import FolderHandler
from file_group import *
from helpers import *
from trash_handler import load_trash_schedule_async, run_trash_check, empty_trash_task



#* Folder Watch Logic
async def run_observer():
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
            await asyncio.sleep(10)
            
            # If you're not currently emptying the trash, attempt to empty it
            if empty_trash_task is None or empty_trash_task.done():
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