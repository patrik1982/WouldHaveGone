from PyQt5.Qt import *

class WIGObject(QAbstractTableModel):
    def __init__(self, obj, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.name = obj.name
        self.properties = obj.properties
        self.methods = []
        #for method in obj.methods:
            #print(method)
            #self.methods.append(WIGFunction.WIGFunction(method))

    def set(self, property, value):
        print(property, value)
        self.properties[property] = value
        print(self.properties)

    def get(self, obj):
        return self.properties[obj]

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
            value = self.properties[key]
            if type(value) == type([]):
                value = '\n'.join(map(str, value))
            else:
                value = str(value)
            return (key, value)[col]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Property'
            if section == 1:
                return 'Value'
        return None
