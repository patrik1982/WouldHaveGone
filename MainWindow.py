import os
import platform
import sys

from PyQt5.Qt import *
import qrc_resources

import lua.parser

import WIGGame

__version__ = "1.0.0"

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__filename = None
        self.__game = WIGGame.WIGGame()

        self.__webview = QWebView()
        self.__webview.setMinimumSize(200, 200)
        #self.__webview.setUrl(QUrl("https://www.openstreetmap.org/"))
        self.setCentralWidget(self.__webview)

        treeDockWindow = QDockWidget("Contents", self)
        treeDockWindow.setObjectName("ContentsDockWidget")
        treeDockWindow.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.__treeWidget = QTreeView()
        self.__treeWidget.setModel(self.__game)
        treeDockWindow.setWidget(self.__treeWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, treeDockWindow)

        infoDockWindow = QDockWidget("Information", self)
        infoDockWindow.setObjectName("InformationDockWidget")
        infoDockWindow.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.__infoWidget = QTreeView()
        infoDockWindow.setWidget(self.__infoWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, infoDockWindow)
        self.__treeWidget.clicked.connect(self.__game.updateInformation)

        self.__game.selectedItemChanged.connect(self.__infoWidget.setModel)

        self.__printer = None

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        fileNewAction = QAction("&New...", self, toolTip="Create an image file", statusTip="Create an image file", icon=QIcon(":/filenew.png"), shortcut=QKeySequence.New, triggered=self.fileNew)
        fileOpenAction = QAction("&Open", self, toolTip="Open an image file", statusTip="Open an image file", icon=QIcon(":/fileopen.png"), shortcut=QKeySequence.Open, triggered=self.fileOpen)
        filePrintAction = QAction("&Print...", self, toolTip="Print an image", statusTip="Print an image", icon=QIcon(":/fileprint.png"), shortcut=QKeySequence.Print, triggered=self.filePrint)
        fileQuitAction = QAction("&Quit", self, toolTip="Close the application", statusTip="Close the application", icon=QIcon(":/filequit.png"), shortcut=QKeySequence.Quit, triggered=self.close)

        self.__fileMenu = self.menuBar().addMenu("&File")
        self.__fileMenuActions = (fileNewAction,
                                  fileOpenAction,
                                  filePrintAction,
                                  fileQuitAction)
        self.__fileMenu.aboutToShow.connect(self.updateFileMenu)

        editMenu = self.menuBar().addMenu("&Edit")

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        fileToolbar.addAction(fileNewAction)
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

    def fileNew(self):
        pass
    def fileOpen(self):
        pass
    def filePrint(self):
        pass

    def loadFile(self, filename):
        p = lua.parser.Parser(filename)
        p.parse()

        for zone in p.zones:
            self.__game.addZone(zone)
        for media in p.media:
            self.__game.addMedia(media)
        for fcn in p.functions:
            self.__game.addFunction(fcn)

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
        filename = "script.txt"
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
