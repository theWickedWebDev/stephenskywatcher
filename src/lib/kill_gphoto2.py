import subprocess
import os
import signal

def killgphoto2Process():
    p = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
    out, _ = p.communicate()

    for line in out.splitlines():
        if b"gvfs-gphoto2-volume-monitor" in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
        if b"gvfsd-gphoto2" in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
