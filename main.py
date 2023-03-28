import sys
import os
import pystray
import PIL.Image
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def __hex_to_dec(hex_num):
    return int(hex_num, 16)

def __is_State_ON():
    output = subprocess.check_output('powercfg /q').decode('utf-8', errors='ignore')
    output = output.split('\n')

    index = 0
    for line in output:
        if 'Subgroup GUID: 4f971e89-eebd-4455-a8de-9e59040e7347' in line and 'Power Setting GUID: 5ca83367-6e45-459f-a27b-476b1d01c936' in output[index + 2]:
            AC = output[index + 12]
            DC = output[index + 13]

            if 'Current AC Power Setting Index:' in AC and 'Current DC Power Setting Index:' in DC:
                hex_AC = AC.strip().split(':')[1].strip()
                dec_AC = __hex_to_dec(hex_AC)

                hex_DC = DC.strip().split(':')[1].strip()
                dec_DC = __hex_to_dec(hex_DC)

                if dec_AC == 0 and dec_DC == 0:
                    return True
                else:
                    return False             
        index += 1   
    return None


if (__is_State_ON()):
    image = PIL.Image.open(resource_path('./images/ON-tray.png'))
else:
    image = PIL.Image.open(resource_path('./images/OFF-tray.png'))


def on_State_Change(icon, item): 
    if (__is_State_ON() == False):
        turn_on_commands = ['powercfg -setacvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 5ca83367-6e45-459f-a27b-476b1d01c936 0', 'powercfg -setdcvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 5ca83367-6e45-459f-a27b-476b1d01c936 0', 'powercfg -SetActive SCHEME_CURRENT']
        for command in turn_on_commands:
            subprocess.check_output(command).decode('utf-8')

        icon.icon = PIL.Image.open(resource_path('./images/ON-tray.png'))
        print ('turned on')

    elif (__is_State_ON() == True):
        turn_on_commands = ['powercfg -setacvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 5ca83367-6e45-459f-a27b-476b1d01c936 1', 'powercfg -setdcvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 5ca83367-6e45-459f-a27b-476b1d01c936 1', 'powercfg -SetActive SCHEME_CURRENT']
        for command in turn_on_commands:
            subprocess.check_output(command).decode('utf-8')
        icon.icon = PIL.Image.open(resource_path('./images/OFF-tray.png'))
        print ('turned off')

    else:
        print ('Error: State is not ON or OFF')


def __on_Exit(icon):
    icon.stop()


if __name__ == "__main__":
    icon = pystray.Icon('LidLocker', image, 'LidLocker By Ran Nahmany' ,menu=pystray.Menu(
    pystray.MenuItem('Change State', on_State_Change),
    pystray.MenuItem('Exit', __on_Exit)
))
    icon.run()