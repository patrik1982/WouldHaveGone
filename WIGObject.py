import UrwigoDecryptor

from PyQt5.Qt import *

class WIGObject(QAbstractTableModel):
    def __init__(self, name=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.properties = {}
        self.subelements = []
        if name:
            self.properties['name'] = name
            self.name = name

    @staticmethod
    def parseStruct(values):
        result = []
        depth = 0
        for k in range(len(values)-1):
            value = values[k+1]
            if value.strip() == '{':
                depth += 1
                result.append(WIGObject.parseStruct(values[k+1:]))
            elif value.strip() == '}':
                depth -= 1
            elif depth == 0:
                val = value.strip()
                if val.endswith(','):
                    val = val[:-1]
                result.append(val)
        return result

    def set(self, property, value):
        if type(value) == type([]): # multi-line assignment, will be a struct in this case
            # Struct assignment
            self.properties[property] = self.parseStruct(value)
        elif type(value) == type(''):
            # String
            if value.startswith('"'):
                self.properties[property] = eval(value)
            else:
                self.properties[property] = UrwigoDecryptor.decrypt(value)
            # remove empty properties
            if self.properties[property] == [] or self.properties[property] == {} or self.properties[property] == '' or self.properties[property] == '{}':
                del self.properties[property]
        else:
            print("Unknown type: '%s'" % (value))
        return

    def get(self, object):
        return self.properties[object]

    def getProps(self):
        return self.properties.keys()

    # QAbstractTableModel methods
    def columnCount(self, parent=QModelIndex()):
        return 2

    def rowCount(self, parent=QModelIndex()):
        return len(self.properties.keys())

    def data(self, index, role=Qt.DisplayRole):
        if (role == Qt.DisplayRole):
            row = index.row()
            col = index.column()
            key = list(self.properties.keys())[row]
            return (key, str(self.properties[key]))[col]
            #if col == 0:
            #    return key
            #elif col == 1:
            #    return str(self.properties[key])
