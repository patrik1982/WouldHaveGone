from WIGObject import WIGObject

class WIGMedia(WIGObject):
    def __init__(self, name):
        WIGObject.__init__(self, name)

        self.data = []

    def set(self, property, value):
        WIGObject.set(self, property, value)

        #return
        # Resources : [['Type = "jpg"', 'Filename = "2f8dae06-b76a-4cbe-86a4-dbd7d86ca9ab.jpg"', 'Directives = {}']]
        # Resources : [{'Filename': '2f8dae06-b76a-4cbe-86a4-dbd7d86ca9ab.jpg', 'Type': 'jpg'}]
        if property == 'Resources':
            newval = []
            values = self.properties[property]
            for value in values:
                thisval = {}
                for keyvalue in value:
                    (prop, val) = keyvalue.split(' = ')
                    if val != "{}":
                        thisval[prop] = eval(val)
                if thisval != {}:
                    newval.append(thisval)
            self.properties[property] = newval
