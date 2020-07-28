# https://build-system.fman.io/pyqt5-tutorial
# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

app = QApplication([])

## icon
icon = QIcon("logo.png")

## system tray app
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

## popup menu
menu = QMenu()
tray.setContextMenu(menu)

## timer action
action = QAction("A menu item")
menu.addAction(action)

## quit action
quit = QAction("Quit")
menu.addAction(quit)
quit.triggered.connect(app.quit)

# label = QLabel('Hello World!')
# label.show()

app.exec_()
