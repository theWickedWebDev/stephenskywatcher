import os
import subprocess
import datetime

from src.util import killgphoto2Process
from ..logger import Logger as _Logger

Logger = _Logger(__name__)


def exec_in_dir(dir, f, args=()):
    cwd = os.getcwd()
    os.chdir(dir)
    f(args)
    os.chdir(cwd)


def gp_proc(cmd):
    try:
        p = subprocess.Popen(
            ["gphoto2"] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = p.communicate()
        if stderr:
            err =  stderr.decode()
            Logger.error('GP_PROC', err)
        return stdout
    except Exception as e:
        if stderr:
            err =  e.decode()
            Logger.error('GP_PROC', err)
            
        pass


def gp_config_current(name):
    try:
        stdout = gp_proc(["--get-config", name])
        if stdout:
            val = ""
            for l in stdout.splitlines():
                line = l.decode()
                if line.startswith("Current: "):
                    val = line.removeprefix("Current: ")

            return val
    except:
        pass


def createDir(loc):
    if os.path.isdir(loc):
        return loc
    try:
        os.makedirs(loc)
        return loc
    except:
        tmpdir = f"/tmp/{datetime.now():%m%d%Y}"
        Logger.warn(f"Failed to create the new directory. Using {tmpdir} instead")
