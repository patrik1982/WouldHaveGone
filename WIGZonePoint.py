from WIGObject import WIGObject

class WIGZonePoint(WIGObject):
    def __init__(self, lat, lon, alt):
        super(WIGZonePoint, self).__init__()
        self.lat = lat
        self.lon = lon
        self.alt = alt

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
