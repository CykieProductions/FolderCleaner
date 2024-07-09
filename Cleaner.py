from watchdog.observers import Observer

import asyncio

from folder_handler import FolderHandler
from file_group import *
from helpers import *

#* Folder Watch Logic
async def run_observer():
    event_handler = FolderHandler(Helpers.join_path_str(Helpers.USER_PATH, "Downloads"), file_groups)
    observer = Observer()
    
    observer.schedule(event_handler, event_handler.tracked_path, recursive=True)
    observer.start()
    # manually look at the target folder to start
    await event_handler.update_folder_async()
    
    try:
        while True:
            #time.sleep(10)
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
def main():
    asyncio.run(run_observer())

#! Guard against outside calls (ex: tests)
if __name__ == "__main__":
    main()