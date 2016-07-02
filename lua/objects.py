import re

from lua import UrwigoDecryptor


class LuaObject(object):
    def __init__(self, name=None):
        self.name = name
        self.properties = {}
        self.methods = {}

    @staticmethod
    def evaluate(value):
        if type(value) == type([]): # multi-line assignment, will be a struct in this case
            # Struct assignment
            return LuaObject.parseStruct(value)
        elif type(value) == type(''):
            # String - normal case
            if value == 'true':
                return True
            elif value == 'false':
                return False
            elif value == '{}':
                return []
            elif value.startswith('ZonePoint'):
                return eval(value)
            elif value.startswith('Distance'):
                return eval(value)
            elif value.startswith('"') and value != '"':
                v = eval(value)
                if v.isdigit():
                    return eval(v)
                else:
                    return v
            else:
                return UrwigoDecryptor.decrypt(value)
        else:
            print("Unknown type: '%s'" % (value))
        return

    @staticmethod
    def parseStruct(values):
        result = []
        depth = 0
        for k in range(len(values)-1):
            value = values[k+1]
            if value.strip() == '{':
                depth += 1
                result.append(LuaObject.parseStruct(values[k+1:]))
            elif value.strip() == '}':
                depth -= 1
            elif depth == 0:
                val = value.strip()
                if val.endswith(','):
                    val = val[:-1]
                val = LuaObject.evaluate(val)
                result.append(val)
        return result

    def set(self, property, value):
        self.properties[property] = LuaObject.evaluate(value)

    def get(self, property):
        return self.properties[property]

    def __str__(self):
        retval = '### OBJECT: %s\n' % self.name
        for property in self.properties:
            retval += '%20s : %s' % (property, self.properties[property])
            if not retval.endswith('\n'):
                retval += '\n'
        for method in self.methods:
            retval += '%20s : %s' % (method, self.methods[method])
            if not retval.endswith('\n'):
                retval += '\n'
        return retval

class LuaFunction(object):
    ctr = 0
    def __init__(self, lines=[]):
        if lines:
            match = re.match("function ([\w\.\:]+)", lines[0])
            self.name = match.group(1) if match else None
        else:
            self.__name = 'unknown%d' % ctr
        self.lines = lines
        LuaFunction.ctr += 1

class ZonePoint(LuaObject):
    cnt = 0
    def __init__(self, lat, lon, alt):
        super(ZonePoint, self).__init__(name = 'pnt%d' % ZonePoint.cnt)
        self.lat = lat
        self.lon = lon
        self.alt = alt
        ZonePoint.cnt += 1

    def __str__(self):
        retval = ''

        lat = self.lat
        lon = self.lon
        if lat > 0:
            retval += 'N'
        else:
            retval += 'S'
        retval += '%02d ' % (lat)
        retval += '%02.3f ' % ((lat % 1.0)*60.0)
        if lon > 0:
            retval += 'E'
        else:
            retval += 'W'
        retval += '%03d ' % (lon)
        retval += '%02.3f' % ((lon % 1.0)*60.0)

        return retval

    def __repr__(self):
        return self.__str__()

class Distance(LuaObject):
    cnt = 0
    def __init__(self, dist, unit):
        super(Distance, self).__init__(name = 'dist%d' % Distance.cnt)
        self.distance = dist
        self.unit = unit
        ZonePoint.cnt += 1

    def __str__(self):
        return 'DIST: %.2f %s' % (self.distance, self.unit)