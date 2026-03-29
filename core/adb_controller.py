import os
import subprocess
import time
import random
from config.settings import (
    TAP_DELAY_MIN, TAP_DELAY_MAX,
    ACTION_DELAY_MIN, ACTION_DELAY_MAX,
    ADB_REMOTE_DIR
)


def adb(device_serial: str, *args) -> str:
    cmd = ['adb', '-s', device_serial] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_devices() -> list:
    output = subprocess.run(['adb', 'devices'], capture_output=True, text=True).stdout
    devices = []
    for line in output.strip().split('\n')[1:]:
        if '\tdevice' in line:
            devices.append(line.split('\t')[0])
    print(f"[ADB] Device connessi: {devices}")
    return devices


def device_serial_from_instance(instance: int) -> str:
    return f"emulator-{5554 + instance * 2}"


def is_device_online(device_serial: str) -> bool:
    return device_serial in get_devices()


def push_video(device_serial: str, local_path: str) -> str:
    try:
        filename = os.path.basename(local_path)
        remote_path = f"{ADB_REMOTE_DIR}/{filename}"
        adb(device_serial, 'shell', 'mkdir', '-p', ADB_REMOTE_DIR)
        adb(device_serial, 'push', local_path, remote_path)
        # Forza scan media gallery
        adb(device_serial, 'shell', 'am', 'broadcast',
            '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE',
            '-d', f'file://{remote_path}')
        print(f"[ADB] Video pushato su {device_serial}: {remote_path}")
        return remote_path
    except Exception as e:
        print(f"[ADB] Errore push su {device_serial}: {e}")
        return ''


def human_tap(device_serial: str, x: int, y: int):
    time.sleep(random.uniform(TAP_DELAY_MIN, TAP_DELAY_MAX))
    adb(device_serial, 'shell', 'input', 'tap', str(x), str(y))


def human_sleep(min_s: float = None, max_s: float = None):
    time.sleep(random.uniform(
        min_s or ACTION_DELAY_MIN,
        max_s or ACTION_DELAY_MAX
    ))
