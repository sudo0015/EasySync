import psutil
import time
import sys
import subprocess
from tkinter import messagebox
from config import cfg

local_device = []
local_letter = []
local_number = 0
mobile_device = []
mobile_letter = []
mobile_number = 0


def update():
    global local_device, local_letter, local_number, mobile_device, mobile_letter, mobile_number
    tmp_local_device, tmp_local_letter = [], []
    tmp_mobile_device, tmp_mobile_letter = [], []
    tmp_local_number, tmp_mobile_number = 0, 0
    try:
        part = psutil.disk_partitions()
    except:
        messagebox.showerror("错误", "发生异常。")
        sys.exit(-1)
    else:
        for i in range(len(part)):
            tmplist = part[i].opts.split(",")
            if len(tmplist) > 1:
                if tmplist[1] == "fixed":
                    tmp_local_number = tmp_local_number + 1
                    tmp_local_letter.append(part[i].device[:2])
                    tmp_local_device.append(part[i])
                else:
                    tmp_mobile_number = tmp_mobile_number + 1
                    tmp_mobile_letter.append(part[i].device[:2])
                    tmp_mobile_device.append(part[i])
        local_device, local_letter = tmp_local_device[:], tmp_local_letter[:]
        mobile_device, mobile_letter = tmp_mobile_device[:], tmp_mobile_letter[:]
        local_number, mobile_number = tmp_local_number, tmp_mobile_number
    return len(part)


if __name__ == "__main__":
    cycle=cfg.ScanCycle.value/10
    now_number = 0
    before_number = update()
    before_letter = local_letter + mobile_letter
    while True:
        now_number = update()
        if (now_number > before_number and len(set(local_letter + mobile_letter).difference(set(before_letter))) == 1):
            str_temp = ''.join(set(local_letter + mobile_letter).difference(set(before_letter)))
            subprocess.Popen("EasySyncUsbService.exe " + str_temp,
                             shell=True)
            before_number = now_number
            before_device = local_device + mobile_letter
            before_letter = local_letter + mobile_letter
        elif (now_number < before_number):
            before_number = now_number
            before_letter = local_letter + mobile_letter
        time.sleep(cycle)
