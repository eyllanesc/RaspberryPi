#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QAction, qApp, QMessageBox

from lib import DHTGPIO, GroupButtonGPIO


class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        layout = QHBoxLayout(self)
        vlayout = QVBoxLayout()

        self.addCustomAction()

        w = QWidget()
        b = GroupButtonGPIO(w)
        b.addButton(18, "Pin 18: ")
        b.addButton(23, "Pin 23: ")
        b.move(w.width()/6, 2*w.height()/3)
        vlayout.addWidget(w)
        layout.addLayout(vlayout)

        d = DHTGPIO()
        layout.addWidget(d)

    def addCustomAction(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        quitAction = QAction("Salir", self, icon=QIcon(":close"), shortcut="Ctrl+Q", triggered=qApp.quit)
        self.addAction(quitAction)
        aboutAction = QAction("Acerca de Qt", self, icon=QIcon(":qt"), shortcut="Ctrl+A", triggered=self.about)
        self.addAction(aboutAction)

    def about(self):
        QMessageBox.aboutQt(None, self.tr("Acerca de Qt"))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Widget()
    w.showFullScreen()
    sys.exit(app.exec_())




