import os
import platform
import sys

from PyQt5.Qt import *
import qrc_resources

import gwc.gwcd

import lua.parser

import WIGGame
import WIGFunction
import WIGMedia

__version__ = "1.0.0"

class WIGMediaViewer(QWidget):
    def __init__(self, *args):
        super(QWidget, self).__init__(*args)

        self.__textWidget = QLabel("<i>No media</i>")
        self.__textWidget.setAlignment(Qt.AlignCenter)

        self.__sourceWidget = QPlainTextEdit("No source")
        self.__sourceWidget.hide()

        self.__imageWidget = QLabel()
        self.__imageWidget.setAlignment(Qt.AlignCenter)
        self.__imageWidget.hide()
        self.__imageLabel = QLabel()
        self.__imageLabel.setAlignment(Qt.AlignCenter)
        self.__imageLabel.hide()
        self.__imageLayout = QVBoxLayout()
        self.__imageLayout.addWidget(self.__imageWidget)
        self.__imageLayout.addWidget(self.__imageLabel)

        self.__layout = QHBoxLayout()
        self.__layout.addWidget(self.__textWidget)
        self.__layout.addWidget(self.__sourceWidget)
        self.__layout.addLayout(self.__imageLayout)
        #self.__layout.addWidget(self.__imageWidget)
        self.setLayout(self.__layout)

    def loadMedia(self, media):
        self.__textWidget.hide()
        self.__sourceWidget.hide()
        self.__imageWidget.hide()
        self.__imageLabel.hide()
        if isinstance(media, WIGFunction.WIGFunction):
            self.__sourceWidget.show()
            self.__sourceWidget.clear()
            self.__sourceWidget.insertPlainText(media.getSource())
            self.__sourceWidget.setReadOnly(True)
        elif isinstance(media, WIGMedia.WIGMedia):
            if media.getType() in ['jpg', 'png']:
                #self.__imageWidget.setText("Would load image %s" % media.getFilename())
                img = QImage.fromData(media.data)
                self.__imageWidget.setPixmap(QPixmap.fromImage(img))
                self.__imageLabel.setText("%s (%d x %d pixels)" % (media.getType().upper(), img.width(), img.height()))
                self.__imageLabel.show()
            else:
                self.__textWidget.setText("Would load media %s (%s)" % (media.name, type(media)))
            self.__imageWidget.show()
        else:
            self.__textWidget.show()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__filename = None
        self.__game = WIGGame.WIGGame()

        self.__html = None

        self.__webview = QWebView()
        self.__webview.setMinimumSize(200, 200)
        QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.setCentralWidget(self.__webview)

        treeDockWindow = QDockWidget("Contents", self)
        treeDockWindow.setObjectName("ContentsDockWidget")
        treeDockWindow.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.__treeWidget = QTreeView()
        self.__treeWidget.setHeaderHidden(True)
        self.__treeWidget.setModel(self.__game)
        self.__treeWidget.setAnimated(True)
        self.__treeWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        treeDockWindow.setWidget(self.__treeWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, treeDockWindow)

        infoDockWindow = QDockWidget("Information", self)
        infoDockWindow.setObjectName("InformationDockWidget")
        infoDockWindow.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.__infoWidget = QTreeView()
        infoDockWindow.setWidget(self.__infoWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, infoDockWindow)

        mediaDockWindow = QDockWidget("Media Viewer", self)
        mediaDockWindow.setObjectName("MediaDockWidget")
        mediaDockWindow.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.__mediaWidget = WIGMediaViewer()
        mediaDockWindow.setWidget(self.__mediaWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, mediaDockWindow)

        self.__treeWidget.selectionModel().selectionChanged.connect(self.__game.updateInformation)
        self.__game.selectedItemChanged.connect(self.__infoWidget.setModel)
        self.__game.selectedItemChanged.connect(self.__mediaWidget.loadMedia)

        self.__printer = None

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        fileOpenAction = QAction("&Open", self, toolTip="Open a cartridge", statusTip="Open a cartridge", icon=QIcon(":/fileopen.png"), shortcut=QKeySequence.Open, triggered=self.fileOpen)
        filePrintAction = QAction("&Print...", self, toolTip="Print cartridge data", statusTip="Print cartridge data", icon=QIcon(":/fileprint.png"), shortcut=QKeySequence.Print, triggered=self.filePrint)
        fileQuitAction = QAction("&Quit", self, toolTip="Close the application", statusTip="Close the application", icon=QIcon(":/filequit.png"), shortcut=QKeySequence.Quit, triggered=self.close)

        self.__fileMenu = self.menuBar().addMenu("&File")
        self.__fileMenuActions = (fileOpenAction,
                                  filePrintAction,
                                  fileQuitAction)
        self.__fileMenu.aboutToShow.connect(self.updateFileMenu)

        editMenu = self.menuBar().addMenu("&Edit")

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        fileToolbar.addAction(fileOpenAction)
        fileToolbar.addAction(filePrintAction)

        helpMenu = self.menuBar().addMenu("&Help")

        editToolbar = self.addToolBar("Edit")

        settings = QSettings()
        self.__recentFiles = settings.value("RecentFiles", type=list)
        size = settings.value("MainWindow/Size", QVariant(QSize(600, 500)), type=QSize)
        self.resize(size)
        position = settings.value("MainWindow/Position", QVariant(QPoint(0, 0)), type=QPoint)
        self.move(position)
        self.restoreState(settings.value("MainWindow/State", type=QByteArray))
        self.setWindowTitle("WouldHaveGone")
        self.updateFileMenu()
        QTimer.singleShot(0, self.loadInitialFile)

    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = os.path.dirname(self.__filename) if self.__filename is not None else "."
        fname = QFileDialog.getOpenFileName(self,
                                "WouldHaveGone - Choose cartridge",
                                dir,
                                "Cartridge files (*.gwc)")[0]
        if fname:
            self.loadFile(fname)

    def filePrint(self):
        pass

    def loadFile(self, filename):
        print(filename)
        files = gwc.gwcd.decompile(filename)
        #return
        filename = "script.txt"
        p = lua.parser.Parser(filename)
        p.parse()

        self.__game.setCartridge(p.cartridge)
        for item in p.items:
            self.__game.addItem(item)
        for zone in p.zones:
            self.__game.addZone(zone)
        for (media, data) in zip(p.media, files['media']):
            self.__game.addMedia(media, data)
        for fcn in p.functions:
            self.__game.addFunction(fcn)
        for obj in p.objects:
            self.__game.addObject(obj)

        self.__html = html = '''<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>WIG Zone Viewer</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

      function initMap() {
        var bounds = new google.maps.LatLngBounds();
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 10,
          center: WIGSTART,
          mapTypeId: google.maps.MapTypeId.TERRAIN
        });

        ZONEDATA
        map.fitBounds(bounds);
        map.panToBounds(bounds);
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key= AIzaSyAhldaQF3P1bKXLJgy__xdUFhcxU1OXE8k &callback=initMap">
    </script>
  </body>
</html>
'''
        zoneCode = ''
        for zone in self.__game.zones:
            zoneCode += zone.getJavaScript()
        wigStart = self.__game.getStartJavaScript()
        self.__html = self.__html.replace('ZONEDATA', zoneCode)
        self.__html = self.__html.replace('WIGSTART', wigStart)
        #self.__webview.setHtml(self.__html)

    def addRecentFile(self, fname):
        if not fname:
            return
        if not fname in self.__recentFiles:
            self.__recentFiles = [fname] + self.__recentFiles
            while len(self.__recentFiles) > 9:
                self.__recentFiles.pop()

    def updateFileMenu(self):
        self.__fileMenu.clear()
        self.__fileMenu.addActions(self.__fileMenuActions[:-1])
        current = self.__filename
        recentFiles = []
        for fname in self.__recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.__fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction("&%d. %s" % (i+1, QFileInfo(fname).fileName()), self, icon=QIcon(":/icon.png"), triggered=self.loadFile)
                action.addData(fname)
                self.__fileMenu.addAction(action)
        self.__fileMenu.addSeparator()
        self.__fileMenu.addAction(self.__fileMenuActions[-1])

    def okToContinue(self):
        return True

    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            filename = QVariant(self.__filename) if self.__filename is not None else QVariant()
            settings.setValue("LastFile", filename)
            recentfiles = QVariant(self.__recentFiles) if self.__recentFiles else QVariant()
            settings.setValue("RecentFiles", recentfiles)
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position", QVariant(self.pos()))
            settings.setValue("MainWindow/State", QVariant(self.saveState()))
        else:
            event.ignore()

    def loadInitialFile(self):
        settings = QSettings()
        filename = settings.value("LastFile", type=str)
        #filename = "script.txt"
        filename = 'C:/Users/Patrik Jakobsson/PycharmProjects/WouldHaveGone/marmorbruket_-_iho.gwc'
        if filename and QFile.exists(filename):
            self.loadFile(filename)

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal=QAction.triggered):
        action = QAction(text, self)
        if icon:
            action.setIcon(QIcon(icon))
        if shortcut:
            action.setShortcut(shortcut)
        if tip:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot:
            pass
        if checkable:
            action.setCheckable(checkable)
        return action


def main():
    app = QApplication(sys.argv)
    app.exec_()

if __name__ == "__main__":
    main()
