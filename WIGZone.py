from WIGObject import WIGObject

class WIGZone(WIGObject):
    def __init__(self, name):
        WIGObject.__init__(self, name)
        self.checked = True

