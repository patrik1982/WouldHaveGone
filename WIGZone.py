from WIGObject import WIGObject

class WIGZone(WIGObject):
    cnt = 1
    def __init__(self, zone=None):
        WIGObject.__init__(self, zone)
        self.checked = True
        WIGZone.cnt += 1

    def getJavaScript(self):
        retval = '''var %s = new google.maps.Polygon({
          paths: [
''' % self.name
        for point in self.get('Points'):
            retval += "            {lat: %f, lng: %f}, \n" % (point.lat, point.lon)
        markerpoint = self.get('OriginalPoint')
        retval += '''          ],
          strokeColor: '#FF0000',
          strokeOpacity: 0.8,
          strokeWeight: 3,
          fillColor: '#FF0000',
          fillOpacity: 0.35
        });
        %s.setMap(map);
        var marker%s = new google.maps.Marker({
          position: {lat: %f, lng: %f},
          map: map,
          title: '%s'
        });
        ''' % (self.name, self.name, markerpoint.lat, markerpoint.lon, self.name)
        for point in self.get('Points'):
            retval += '            bounds.extend(new google.maps.LatLng("%f","%f")); \n' % (point.lat, point.lon)
        return retval

