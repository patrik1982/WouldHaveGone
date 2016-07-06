from WIGObject import WIGObject

class WIGFunction(WIGObject):
    cnt = 1
    def __init__(self, obj=None):
        WIGObject.__init__(self, obj)
        self.checked = True
        WIGFunction.cnt += 1
        self.source = '\n'.join(obj.lines)

    def getSource(self):
        return self.source

