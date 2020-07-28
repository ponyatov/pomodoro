# https://build-system.fman.io/pyqt5-tutorial
# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

app = QApplication([])

## icon
planning = QIcon('planning.png')
triangle = QIcon('triangle.png')
icon = planning

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

import threading, queue
import time, datetime as dt

## thread stop signaling queue
stopq = queue.Queue(1)

## timer background function (clicks every 1 sec)
def upd():
    icon = [planning, triangle]
    idx = 0
    timer = dt.timedelta(minutes=5)#15
    stopt = dt.timedelta(minutes=0)
    while True:
        try:
            stopq.get(timeout=1)
            break
        except queue.Empty:
            timer -= dt.timedelta(minutes=1)#seconds=1)
            if timer < stopt:
                break
            print('%s' % timer)
            tray.setToolTip(time.strftime('%H:%M:%S', time.localtime()))
            tray.setIcon(icon[idx % 2])
            idx += 1


## timer background thread
th = threading.Thread(target=upd)
th.start()


app.exec_()
stopq.put('stop')
th.join()
