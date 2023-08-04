import sys
import time
import subprocess

import psutil


def countdown(text, t, interrupt=None, shutdown=False):
    while t:
        t -= 1
        print(f"{text} {t} sec.", end='\r')
        if interrupt and interrupt():
            break
        time.sleep(1)
    if shutdown:
        sys.exit()


def launch_process(args):
    try:
        subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
    except Exception as e:
        countdown(f'{e} "{args}", terminate in', 10, shutdown=True)


def get_active_processes(proc_name_list):
    res, sample = [], [proc.lower() for proc in proc_name_list]
    for process in psutil.process_iter(['name']):
        if process.info['name'].lower() in sample:
            res.append(process)
    return res


def check_game_status(proc_name_list):
    sample = [proc.lower() for proc in proc_name_list]
    for process in get_active_processes(proc_name_list):
        if process.name().lower() in sample:
            sample.remove(process.name().lower())
    if sample:
        return False
    else:
        return True


def get_main_process(proc_name_list):
    highest, process = 0, None
    for proc in get_active_processes(proc_name_list):
        rss = proc.memory_info().rss
        if rss > highest:
            highest = rss
            process = proc
    return process
