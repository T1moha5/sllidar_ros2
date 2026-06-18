"""Автовыбор USB-порта SLLIDAR (CP210x / Slamtec)."""

import os
import subprocess

LIDAR_VID_PIDS = [
    ('10c4', 'ea60'),
    ('10c4', 'ea61'),
    ('10c4', 'ea62'),
    ('10c4', 'ea63'),
    ('10c4', 'ea64'),
    ('10c4', 'ea65'),
    ('10c4', 'ea66'),
]


def find_lidar_port():
    try:
        for i in range(10):
            port = f'/dev/ttyUSB{i}'
            if not os.path.exists(port):
                continue
            result = subprocess.run(
                ['udevadm', 'info', '-q', 'property', '-n', port],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                continue
            props = result.stdout
            for vid, pid in LIDAR_VID_PIDS:
                if f'ID_VENDOR_ID={vid}' in props and f'ID_MODEL_ID={pid}' in props:
                    return port
        for i in range(10):
            port = f'/dev/ttyUSB{i}'
            if os.path.exists(port):
                return port
    except OSError:
        pass
    return '/dev/ttyUSB1'
