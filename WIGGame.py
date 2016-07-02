import re

from PyQt5.Qt import *

from WIGZone import WIGZone
from WIGObject import WIGObject

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

        self.__rootNode.appendRow(self.__cartridge)
        self.__rootNode.appendRow(self.__items)
        self.__rootNode.appendRow(self.__media)
        self.__rootNode.appendRow(self.__zones)
        self.__rootNode.appendRow(self.__functions)
        self.__rootNode.appendRow(self.__objects)

        self.__info = {}

    def updateInformation(self, index):
        item = self.itemFromIndex(index)
        parent = item.parent()
        if parent:
            path = parent.text() + item.text()
            self.selectedItemChanged.emit(self.__info[path])


    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 1

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section == 0:
            return 'Name'
        return None

    def addZone(self, zone):
        z = WIGZone(zone)
        zoneitem = QStandardItem(z.name)
        zoneitem.setCheckable(True)
        zoneitem.setCheckState(Qt.Checked)
        self.__zones.appendRow(zoneitem)
        self.__info[self.__zones.text() + z.name] = z

    def addMedia(self, media):
        pass
        m = WIGObject(media)
        mediaitem = QStandardItem(m.name)
        self.__media.appendRow(mediaitem)
        self.__info[self.__media.text() + m.name] = m

    def addFunction(self, function):
        pass
