from lua.objects import *

class Parser(object):
    def __init__(self, filename=None):
        self.src = [line.rstrip() for line in open(filename, 'r')]
        self.items = []
        self.media = []
        self.zones = []
        self.functions = []
        self.cartridge = None
        self.objects = []

    def parse(self):
        inFunction = False
        inAssignment = 0

        reFunction = re.compile('function ([\w\.\:]+)\((\w*)\)')
        reMedia = re.compile('(\w+) = Wherigo.ZMedia\((\w+)\)')
        reCartridge = re.compile('(\w+) = Wherigo.ZCartridge')
        reZone = re.compile('(\w+) = Wherigo.Zone\((\w+)\)')
        reAssignment = re.compile('([\w\.\:]+) = (\S+.*)$')
        reProperty = re.compile('(\w+)\.(\w+)')

        nametable = {}

        currentItem = []
        for line in self.src:
            matchMedia = reMedia.match(line)
            matchCartridge = reCartridge.match(line)
            matchZone = reZone.match(line)
            matchAssignment = reAssignment.match(line)
            matchFunction = reFunction.match(line)

            if '_AcK("' in line:
                pass
            dline = UrwigoDecryptor.decrypt(line)
            if '_AcK("' in line:
                pass
            currentItem.append(dline)

            assigmentDone = False

            if matchCartridge:
                self.name = matchCartridge.group(1)
                cart = LuaObject(self.name)
                nametable[self.name] = cart
                self.cartridge = cart

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
                    if 'nput' in currentItem[0]:
                        pass
                    self.functions.append(LuaFunction(currentItem.copy()))


            if matchMedia:
                (name, cartridge) = matchMedia.groups()
                media = LuaObject(name)
                self.media.append(media)
                nametable[name] = media

            elif matchZone:
                (name, cartridge) = matchZone.groups()
                zone = LuaObject(name)
                self.zones.append(zone)
                nametable[name] = zone

            else:
                # Handle assignments. Use counter for block level. Assumes braces are on otherwise empty lines
                if inAssignment == 0 and matchAssignment:
                    (objec, value) = matchAssignment.groups()
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
                    matchProperty = reProperty.match(objec)
                    if matchProperty:
                        (obj, property) = matchProperty.groups()
                        if obj in nametable.keys():
                            nametable[obj].set(property, value)
                        else:
                            o = LuaObject(obj)
                            self.objects.append(o)
                            nametable[obj] = o


        fcns = self.functions.copy()
        for fcn in fcns:
            if fcn.name.count(':') == 1:
                (o, m) = fcn.name.split(':')
                if o in nametable:
                    fcn.name = m
                    nametable[o].methods[m] = (fcn)
                    self.functions.remove(fcn)
            elif fcn.name.count('.') == 2:
                (o, c, m) = fcn.name.split('.')
                if o in nametable:
                    fcn.name = m
                    nametable[o].get(c).append(m)
                    self.functions.remove(fcn)
            elif fcn.name.count('.') == 1:
                (o, m) = fcn.name.split('.')
                if o in nametable:
                    fcn.name = m
                    nametable[o].methods[m] = fcn
                    self.functions.remove(fcn)
            else:
                pass
