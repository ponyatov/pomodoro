# https://build-system.fman.io/pyqt5-tutorial
# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/

import os, sys, time, datetime as dt

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

app = QApplication([])

## icon
logo = QIcon('logo.png')
nologo = QIcon('nologo.png')

## system tray app
tray = QSystemTrayIcon()
tray.setIcon(logo)
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

## thread stop signaling queue
stopq = queue.Queue(1)

## timer background function (clicks every 1 sec)
def upd():
    idx = 0
    flips = [nologo, logo]
    timer = dt.timedelta(minutes=15)#15
    stopt = dt.timedelta(minutes=0)
    while True:
        try:
            stopq.get(timeout=1)
            tray.setIcon(logo)
            tray.showMessage(sys.argv[0], '', logo)
            break
        except queue.Empty:
            timer -= dt.timedelta(seconds=1)#minutes=1)#seconds=1)
            if timer < stopt:
                stopq.put('stop')
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
