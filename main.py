import sys

import MainWindow

from PyQt5.Qt import *

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("patrik1982soft")
    app.setOrganizationName("patrik1982soft.eu")
    app.setApplicationName("WouldHaveGone")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow.MainWindow()
    form.show()
    return app.exec_()

if __name__ == '__main__':
    main()