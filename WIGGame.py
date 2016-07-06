import re

from PyQt5.Qt import *

from WIGZone import WIGZone
from WIGObject import WIGObject
from WIGFunction import WIGFunction

class WIGGame(QStandardItemModel):
    selectedItemChanged = pyqtSignal(QAbstractTableModel)

    def __init__(self, parent=None):
        QStandardItemModel.__init__(self)

        self.__rootNode = self.invisibleRootItem()

        self.__cartridge = QStandardItem("Cartridge")
        self.__functions = QStandardItem("Functions")
        self.__objects= QStandardItem("Objects")
        self.__items = QStandardItem("Items")
        self.__media = QStandardItem("Media")
        self.__zones = QStandardItem("Zones")
        self.zones = []
        self.cartridge = None

        self.__rootNode.appendRow(self.__cartridge)
        self.__rootNode.appendRow(self.__items)
        self.__rootNode.appendRow(self.__media)
        self.__rootNode.appendRow(self.__zones)
        self.__rootNode.appendRow(self.__functions)
        self.__rootNode.appendRow(self.__objects)

        self.info = {}

    def updateInformation(self, index):
        item = self.itemFromIndex(index)
        parent = item.parent()
        if parent:
            path = parent.text() + item.text()
            self.selectedItemChanged.emit(self.info[path])

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 1

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section == 0:
            return 'Name'
        return None

    def setCartridge(self, cartridge):
        self.cartridge = WIGObject(cartridge)

    def addZone(self, zone):
        z = WIGZone(zone)
        zoneitem = QStandardItem(z.name)
        zoneitem.setCheckable(True)
        zoneitem.setCheckState(Qt.Checked)
        self.__zones.appendRow(zoneitem)
        self.info[self.__zones.text() + z.name] = z
        self.zones.append(WIGZone(zone))

    def addMedia(self, media):
        m = WIGObject(media)
        mediaitem = QStandardItem(m.name)
        self.__media.appendRow(mediaitem)
        self.info[self.__media.text() + m.name] = m

    def addFunction(self, function):
        f = WIGFunction(function)
        functionitem = QStandardItem(f.name)
        self.__functions.appendRow(functionitem)
        self.info[self.__functions.text() + f.name] = f

    def addItem(self, item):
        i = WIGObject(item)
        itemitem = QStandardItem(i.name)
        self.__item.appendRow(itemitem)
        self.info[self.__item.text() + i.name] = i

    def addObject(self, obj):
        o = WIGObject(obj)
        objectitem = QStandardItem(o.name)
        self.__objects.appendRow(objectitem)
        self.info[self.__objects.text() + o.name] = o

    def getStartJavaScript(self):
        point = self.cartridge.get('StartingLocation')
        return '{lat: %f, lng: %f}' % (point.lat, point.lon)
