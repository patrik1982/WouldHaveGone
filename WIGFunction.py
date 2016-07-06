from WIGObject import WIGObject

class WIGFunction(WIGObject):
    cnt = 1
    def __init__(self, zone=None):
        WIGObject.__init__(self, zone)
        self.checked = True
        WIGFunction.cnt += 1

    def getSource(self):
        retval = ''
        return retval

