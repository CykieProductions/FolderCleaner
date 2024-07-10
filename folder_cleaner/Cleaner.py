from watchdog.observers import Observer

import asyncio

from .folder_handler import FolderHandler
from .file_group import *
from .helpers import *
from .trash_handler import try_empty_trash

#* Folder Watch Logic
async def run_observer():
    downloads_handler = FolderHandler(Helpers.join_path_str(Helpers.USER_PATH, "Downloads"), file_groups)
    downloads_observer = Observer()
    
    downloads_observer.schedule(downloads_handler, downloads_handler.tracked_path, recursive=False)
    downloads_observer.start()
    # manually check the target folder to start
    await downloads_handler.update_folder_async()
    
    print("Before trash")
    empty_trash_task = asyncio.create_task(try_empty_trash())
    print("After trash")
    
    try:
        while True:
            #time.sleep(10)
            await asyncio.sleep(10)
            
            if empty_trash_task is not None and empty_trash_task.done():
                print("Check trash")
                #TODO - Schedule a trash check
                pass
            
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