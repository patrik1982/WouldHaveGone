import sys

import MainWindow

from PyQt5.Qt import *

import lua.parser

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
    if True and False:
        p = lua.parser.Parser("script.txt")
        p.parse()
        print(p.items)
        for i in p.items:
            pass
            print(i)
        print(p.zones)
        for i in p.zones:
            print(i)
            pass
        print(p.media)
        for i in p.media:
            pass
            print(i)
        print(p.functions)
        for i in p.functions:
            print(i)
        print(p.objects)
        for i in p.objects:
            pass
            print(i)
