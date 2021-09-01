# -*- coding: utf-8 -*-

from log import task_logger,local
import time
import sys

class myThread(object):
    def execute(self, task_id):
        print("run task_id:{}".format(task_id))
        local.log_extra =  {"workid": "sunThread", "taskid": task_id}
        task_logger.info("run in sunThread")
        time.sleep(1)
