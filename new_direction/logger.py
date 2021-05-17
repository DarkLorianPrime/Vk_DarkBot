import os
import time
import traceback


def logger(info=None):
    rw = open(f'{os.getcwd()}/Logs.log', 'a+')
    if info is not None:
        rw.write(f'{"=" * 10}\n')
        rw.write(f'{time.strftime("/%H:%M:%S/")} [INFO] {info} \n')

    def logger_dec(fn):
        def logger_wrap(*args):
            rw = open(f'{os.getcwd()}/Logs.log', 'a+')
            rw.write(f'{"=" * 10}\n')
            try:
                returned = fn(*args)
                print(f'{fn.__name__} successful execute.')
                rw.write(f'{time.strftime("/%H:%M:%S/")} [LOADED] {fn.__name__} successful execute. \n')
            except Exception:
                returned = args
                rw.write(
                    f'{time.strftime("/%H:%M:%S/")} [ERROR] Function [{fn.__name__}] Loading error: \n {traceback.format_exc()} \n')
                print(
                    '[ERROR]Error, look at the information in the logs!\n[ERROR]Function returned the original value!')
            rw.write(f'{"=" * 10}\n')
            rw.close()
            return returned

        return logger_wrap

    return logger_dec
