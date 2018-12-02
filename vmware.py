import subprocess
from pathlib import *

class vmware(object):
    vmrunpath = None
    output = None
    def __init__(self, vmwarepath):
        vmwarepath = vmwarepath.replace("\"", "")
        vmwarepath = vmwarepath.replace("\'", "")
        self.vmrunpath = Path(vmwarepath).joinpath("vmrun.exe")
    def updateOutput(self):
        output = subprocess.run([str(self.vmrunpath), "list"], stdout=subprocess.PIPE)
        output = output.stdout.decode("utf-8")
        output = output.split("\r\n")
        del output[-1]
        self.output = output
    def runCount(self):
        return len(self.output) - 1
    def isRunning(self):
        if self.runCount() > 0:
            return True
        else:
            return False
    def getRunningVMPath(self, index = None):
        output = self.output
        del output[0]
        if index != None:
            return output[index]
        else:
            return output
    def getVMProperty(self, path, property):
        vmx = Path(path)
        value = None
        for line in vmx.read_text().split("\n"):
            if property in line:
                value = line[len(property) + 4:][:-1]
                break
        return value
    def getVMName(self, path):
        return self.getVMProperty(path, "displayName")
    def getRunningVMProperty(self, index, property):
        return self.getVMProperty(self.getRunningVMPath(index), property)
    def getRunningVMName(self, index):
        return self.getRunningVMProperty(index, "displayName")