import re

from PyQt5.Qt import *

import UrwigoDecryptor

from WIGFunction import WIGFunction
from WIGMedia import WIGMedia
from WIGZone import WIGZone

class TreeNode(object):
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.subnodes = self._getChildren()

    def _getChildren(self):
        raise NotImplementedError()

class TreeModel(QAbstractItemModel):
    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.rootNodes = self._getRootNodes()

    def _getRootNodes(self):
        raise NotImplementedError()

    def index(self, row, column, parent):
        if not parent.isValid():
            return self.createIndex(row, column, self.rootNodes[row])
        parentNode = parent.internalPointer()
        return self.createIndex(row, column, parentNode.subnodes[row])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)

    def reset(self):
        self.rootNodes = self._getRootNodes()
        QAbstractItemModel.reset(self)

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.rootNodes)
        node = parent.internalPointer()
        return len(node.subnodes)

class NamedElement(object): # your internal structure
    def __init__(self, name, subelements):
        self.name = name
        self.subelements = subelements

class NamedNode(TreeNode):
    def __init__(self, ref, parent, row):
        self.ref = ref
        TreeNode.__init__(self, parent, row)

    def _getChildren(self):
        return [NamedNode(elem, self, index) for index, elem in enumerate(self.ref.subelements)]

class WIGGame(TreeModel):
    def __init__(self, src_lines, parent=None):
        self.src = src_lines
        self.items = []
        self.media = []
        self.zones = []
        self.functions = []
        self.name = None

        self.parse()
        self.rootElements = [NamedElement("Items", self.items[:]),
                             NamedElement("Media", self.media[:]),
                             NamedElement("Functions", self.functions[:]),
                             NamedElement("Zones", self.zones[:])]
        TreeModel.__init__(self)

    def _getRootNodes(self):
        return [NamedNode(elem, None, index) for index, elem in enumerate(self.rootElements)]


    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole and index.column() == 0:
            return node.ref.name
        if role == Qt.CheckStateRole and index.column() == 1:
            pass
            #return node.ref.checked
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section == 0:
            return 'Name'
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section == 1:
            return 'Visible'
        return None

    def parse(self):
        inFunction = False
        inAssignment = 0

        reFunction = re.compile('function ([\w\.\:]+)\((\w*)\)')
        reMedia = re.compile('(\w+) = Wherigo.ZMedia\((\w+)\)')
        reCartridge = re.compile('(\w+) = Wherigo.ZCartridge')
        reZone = re.compile('(\w+) = Wherigo.Zone\((\w+)\)')
        reAssignment = re.compile('([\w\.\:]+) = (\S+.*)$')
        reProperty = re.compile('(\w+).(\w+)')

        nametable = {}

        currentItem = []
        for line in self.src:
            matchMedia = reMedia.match(line)
            matchCartridge = reCartridge.match(line)
            matchZone = reZone.match(line)
            matchAssignment = reAssignment.match(line)
            matchFunction = reFunction.match(line)

            currentItem.append(line)

            assigmentDone = False

            if matchCartridge:
                self.name = matchCartridge.group(1)

            if not inFunction and matchFunction:
                inFunction = True
                fcnname = matchFunction.group(1)
                currentItem = [line]
            elif inFunction:
                if 'local dtable = ' in line:
                    dtable = line[line.find('local dtable = ') + 15:]
                    UrwigoDecryptor.setLuaKeyString(dtable)
                    UrwigoDecryptor.setDecryptFcnName(fcnname)
                if line == 'end':
                    inFunction = False
                    self.functions.append(WIGFunction(currentItem))


            if matchMedia:
                (name, cardridge) = matchMedia.groups()
                media = WIGMedia(name)
                self.media.append(media)
                nametable[name] = media

            elif matchZone:
                (name, cardridge) = matchZone.groups()
                zone = WIGZone(name)
                self.zones.append(zone)
                nametable[name] = zone

            else:
                # Handle assignments. Use counter for block level. Assumes braces are on otherwise empty lines
                if inAssignment == 0 and matchAssignment:
                    (object, value) = matchAssignment.groups()
                    if value == '{':
                        currentItem = [value]
                        inAssignment = 1
                    else:
                        assigmentDone = True
                elif inAssignment > 0 and line.strip() == '{':
                    inAssignment += 1
                elif inAssignment > 0 and line.strip() == '}':
                    inAssignment -= 1
                    # Closing brace?
                    if inAssignment == 0:
                        value = currentItem[:]
                        assigmentDone = True
                if assigmentDone:
                    matchProperty = reProperty.match(object)
                    if matchProperty:
                        (object, property) = matchProperty.groups()
                        if object in nametable.keys():
                            nametable[object].set(property, value)


    def __str__(self):
        retval = ''

        retval += 'Name: %s\n' % (self.name)

        for media in self.media:
            retval += 'Media: %s\n' % (media.get('name'))
            for prop in media.getProps():
                retval +='  %s : %s\n' % (prop, media.get(prop))
            pass

        for zone in self.zones:
            retval += 'Zone: %s\n' % (zone.get('name'))
            for prop in zone.getProps():
                pass
                #etval +='  %s : %s\n' % (prop, zone.get(prop))
            pass

        for function in self.functions:
            #print(function.name)
            pass

        return retval

#    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
#        return 1

#    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
#        return 3
