from WIGObject import WIGObject

import re

reProp = re.compile('(\w+) = "(\S+)"')

class WIGMedia(WIGObject):
    cnt = 1
    def __init__(self, obj, data):
        WIGObject.__init__(self, obj)

        resources = {}
        self.data = data
        if 'Resources' in self.properties.keys():
            resource = self.properties['Resources'][0]   # Assume only one resource ... I have never seen the opposite...
            for item in resource:
                matchProp = reProp.match(item)
                if matchProp:
                    (key, value) = matchProp.groups()
                    resources[key] = value
            self.properties['Resources'] = resources


    def getType(self):
        return self.get('Resources')['Type']

    def getFilename(self):
        return self.get('Resources')['Filename']
