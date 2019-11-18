from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import view

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("KTTM-1")
        self.setCentralWidget(widget)
        self.initMenu()

    def initMenu(self):
        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        methodMenu = menu.addMenu("Method")
        methodsGroup =  QtWidgets.QActionGroup(self)
        vercleAction = QtWidgets.QAction('Verle', methodsGroup, checkable=True)
        odintAction = QtWidgets.QAction('ODINT', methodsGroup, checkable=True)
        methodMenu.addAction(vercleAction)
        methodMenu.addAction(odintAction)        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow(view.MainWidget())
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())