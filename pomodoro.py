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
    idx = 0
    flips = [planning, triangle]
    timer = dt.timedelta(minutes=5)#15
    stopt = dt.timedelta(minutes=0)
    while True:
        try:
            stopq.get(timeout=1)
            tray.setIcon(icon)
            break
        except queue.Empty:
            timer -= dt.timedelta(minutes=1)#minutes=1)#seconds=1)
            if timer < stopt:
                tray.setIcon(icon)
                break
            print('%s' % timer)
            tray.setToolTip('%s' % timer)
            tray.setIcon(flips[idx % len(flips)])
            idx += 1


## timer background thread
th = threading.Thread(target=upd)

def go():
    global th
    if th.is_alive():
        stopq.put('stop')
        time.sleep(1)
    th = threading.Thread(target=upd)
    th.start()


action.triggered.connect(go)


app.exec_()
if th.is_alive():
    stopq.put('stop')
    th.join()
