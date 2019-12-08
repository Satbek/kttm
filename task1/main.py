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
        methodsGroup =  QtWidgets.QActionGroup(self)
        methodsGroup.triggered.connect(self.centralWidget().view.setSolver)

        verleAction = QtWidgets.QAction('Simple Verle', methodsGroup, checkable=True)
        odeintAction = QtWidgets.QAction('ODEINT', methodsGroup, checkable=True)
        verleAction.setStatusTip('Verle algotithm based solver')
        odeintAction.setStatusTip('scipy.integrate.odeint based solver')
        verleAction.setChecked(True)

        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        methodMenu = menu.addMenu("Method")
        methodMenu.addAction(verleAction)
        methodMenu.addAction(odeintAction)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow(view.MainWidget())
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())