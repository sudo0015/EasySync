from winotify import Notification, Notifier, audio
import time
import sys
from win32api import GetVolumeInformation

def GetDriveName():
    if GetVolumeInformation(drive)[0] != '':
        return GetVolumeInformation(drive)[0]
    else:
        return "U盘"

if __name__ == '__main__':
    drive = sys.argv[1]
    toast = Notification(app_id="EasySync", title="同步完成", msg=GetDriveName()+' ('+drive+')', icon="",
                         duration="long")
    toast.set_audio(audio.Default, loop=False)
    toast.show()
    time.sleep(5)
    Notifier.clear(toast)
