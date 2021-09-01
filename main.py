# -*- coding: utf-8 -*-
"""
@file: label_worker.py
@time: 2021/8/25 3:54 下午
@author: szy
@instruction:
"""
import sys
import time
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor,as_completed

from log import task_logger,local
from thread import myThread

def main(argv):
    task_logger.debug("not set workid: main-thread ")
    logging.getLogger('task_logger').debug("test logging.getLogger ")

    local.log_extra = {"workid": "main-thread", "taskid":0}
    task_logger.warning("use workid: main-thread")
    task_logger.warning("test format {}".format(datetime.now()))


    log_extra = {"workid": "private-workid", "taskid":0}
    task_logger.critical("use private workid", extra = log_extra)

    task_list = [1,2,3,4]

    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Start the load operations and mark each future with its URL
        futures = {executor.submit(myThread().execute, task_id): task_id for task_id in task_list}
        for future in as_completed(futures):
            task_id = futures[future]
            print(task_id)

if __name__ == '__main__':
    main(sys.argv)
