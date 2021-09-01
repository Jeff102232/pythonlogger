# -*- coding: utf-8 -*-

import logging
import datetime
import logging.handlers
import threading
import sys,os

#LOG_FORMAT = "%(asctime)s - %(levelname)s - %(process)d - %(thread)d -%(pathname)s/%(filename)s:%(lineno)d |  %(message)s"
LOG_FORMAT = "%(asctime)s %(levelname)s %(process)d-%(thread)d | %(filename)s:%(lineno)d | %(workid)s:%(taskid)d | %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

#logging.basicConfig(filename='jeff.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
rf_handler = logging.handlers.TimedRotatingFileHandler('task_schedular.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
rf_handler.setLevel(logging.DEBUG)
rf_handler.setFormatter(logging.Formatter(LOG_FORMAT,DATE_FORMAT))

local = threading.local()
local.log_extra = {"workid": "workid_dedault", "taskid":0}

if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else: #pragma: no cover
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back

#https://stackoverflow.com/questions/19615876/showing-the-right-funcname-when-wrapping-logger-functionality-in-a-custom-class
_loggingfile = os.path.normcase(logging.__file__)
if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

class TaskLogger(logging.getLoggerClass()):
    def __init__(self, name):
        logging.Logger.__init__(self, name)
    #Modified slightly from cpython's implementation https://github.com/python/cpython/blob/master/Lib/logging/__init__.py#L1374
    def findCaller(self, stack_info=False, stacklevel=2):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    def debug(self, msg, *args, **kwargs):
        options = {'extra' : local.log_extra,}
        options.update(kwargs)
        super().debug(msg, *args, **options)
    def info(self, msg, *args, **kwargs):
        options = {'extra' : local.log_extra,}
        options.update(kwargs)
        super().info(msg, *args, **options)
    def warning(self, msg, *args, **kwargs):
        options = {'extra' : local.log_extra,}
        options.update(kwargs)
        super().warning(msg, *args, **options)
    def critical(self, msg, *args, **kwargs):
        options = {'extra' : local.log_extra,}
        options.update(kwargs)
        super().critical(msg, *args, **options)
    def exception(self, msg, *args, **kwargs):
        options = {'extra' : local.log_extra,}
        options.update(kwargs)
        super().exception(msg, *args, **options)

logging.setLoggerClass(TaskLogger)
task_logger = logging.getLogger('task_logger')
task_logger.addHandler(rf_handler)
task_logger.setLevel(logging.DEBUG)
