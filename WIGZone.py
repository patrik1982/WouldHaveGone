from WIGObject import WIGObject
from WIGZonePoint import WIGZonePoint

class WIGZone(WIGObject):
    def __init__(self, name):
        WIGObject.__init__(self, name)

    def set(self, property, value):
        WIGObject.set(self, property, value)

        if property in self.properties:
            val = self.properties[property]
            if type(val) == type('') and val.startswith('ZonePoint'):
                self.properties[property] = eval('WIG%s' % (value))
            if type(val) == type([]):
                v = []
                for element in val:
                    if element.startswith('ZonePoint'):
                        v.append(eval('WIG%s' % (element)))
                if v != []:
                    self.properties[property] = v
                else:
                    del self.properties[property]
