import subprocess
from enum import Enum
from ...logger import Logger as _Logger
from ..util import gp_proc, gp_config_current

Logger = _Logger(__name__)

class Config:
    name: str
    
    def __init__(self, name):
        self.log  = _Logger(__name__)
        self.name = name

    def get(self): 
        try:
            return gp_config_current(self.name)
        except:
            self.log.error('Failed to set camera config ' + self.name)

    def set(self, enum: Enum):
        try:
            gp_proc(["--set-config", f"{self.name}={enum.value}"])
            self.log.set_config(self.name, enum.value)
        except:
            self.log.error('Failed to set camera config ' + self.name)

    def options(self):
        try:
            stdout = gp_proc(['--get-config', self.name])
            if (stdout):
                opts = []
                lines = stdout.splitlines()
                for l in lines:
                    line = l.decode()
                    if (line.startswith('Choice: ')):
                        opts.append(' '.join(line.removeprefix('Choice: ').split()[1:]))
                return opts

        except:
            self.log.error('Failed to retrieve options for ' + self.name)