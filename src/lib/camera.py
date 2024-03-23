import sh
from sh import gphoto2 as gp

from ..logger import Logger as _Logger
from .presets.preset import ConfigPreset
from .enums import Config, SHUTTER, CUSTOM_FUNC, CANON_FOLDER
from .util import exec_in_dir, gp_config_current
import subprocess
import os
import signal


Logger = _Logger(__name__)


def killgphoto2Process():
    p = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        Logger.error(err)

    for line in out.splitlines():
        if b"gvfs-gphoto2-volume-monitor" in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
        if b"gvfsd-gphoto2" in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


class Camera:
    name: str
    lens: str
    _folder: str

    def __init__(self):
        self.log = _Logger(__name__)
        #
        self.iso = Config("iso")
        self.aperture = Config("aperture")
        self.shutterspeed = Config("shutterspeed")
        self.drivemode = Config("drivemode")
        self.capturetarget = Config("capturetarget")
        self.aeb = Config("aeb")
        self.bracketmode = Config("bracketmode")
        self.picturestyle = Config("picturestyle")
        self.autoexposuremode = Config("autoexposuremode")
        self.continuousaf = Config("continuousaf")
        self.whitebalance = Config("whitebalance")
        self.imageformat = Config("imageformat")
        self.mirrorlockstatus = Config("mirrorlockstatus")
        self.mirrordownstatus = Config("mirrordownstatus")
        self.evfmode = Config("evfmode")
        self.output = Config("output")
        self.viewfinder = Config("viewfinder")
        self.bracketmode = Config("bracketmode")
        self.customfuncex = Config("customfuncex")
        #
        self._setCameraDetails()
        self.log.detail("Initialized Camera", f"{self.name} // {self.lens}")

    def _setCameraDetails(self):
        self.name = gp_config_current("cameramodel")
        self.lens = gp_config_current("lensname")
        self._folder = self._get_folder()

    def _get_folder(self):
        # TODO:
        return CANON_FOLDER

    def config(self, configs):  # configs: List[(Config, Enum)]
        try:
            cmd = []
            for k, v in configs:
                cmd.append("--set-config")
                cmd.append(f"{k.name}={v.value}")
            gp(cmd)
            for k, v in configs:
                self.log.set_config(k.name, v.value)
        except Exception as e:
            self.log.error("Error setting Camera.config", e)

    def set_preset(self, preset: ConfigPreset):
        try:
            cmd = []
            for k, v in preset.list:
                cmd.append("--set-config")
                cmd.append(f"{k.name}={v.value}")
            gp(cmd)
            self.log.action("Camera Preset set", preset.name)
            for k, v in preset.list:
                self.log.set_config(k.name, v.value)

        except sh.ErrorReturnCode_1 as e:
            if "No camera found" in e.stderr.decode():
                self.log.error("NO CAMERA")
                self.log.debug(e.stderr.decode())
            if "Could not claim the USB device" in e.stderr.decode():
                self.log.warn("Attempting to reset gphoto")
                killgphoto2Process()
                self.set_preset(preset)
            self.log.error("Error setting Camera Preset")

    def delete_all(self):
        try:
            gp(["--folder", self._folder, "-R", "--delete-all-files"])
            self.log.action("Deleted all files on card", self._folder)
        except:
            self.log.error("Failed to delete all images on card")

    def mirror_lockup(self, enabled: bool):
        lock = (
            CUSTOM_FUNC.MIRROR_LOCK_ENABLED
            if enabled
            else CUSTOM_FUNC.MIRROR_LOCK_DISABLED
        )
        gp(["--set-config", f'customfuncex="{lock}"'])

    def download(self, dir):
        # TODO: Should this go in into camera? Makes it annoying b/c we need dir
        cmd = ["--get-all-files", "--force-overwrite"]

        exec_in_dir(dir, gp, cmd)
        self.log.action("Downloaded all files", dir)
