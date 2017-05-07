# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QWidget


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.mModified = True
        self.mPixmap = QPixmap()
        self.value_background = True

    def draw_background(self, painter):
        pass

    def draw_value(self, painter):
        pass

    def draw_back(self):
        if self.mModified or self.mPixmap.size() != self.size():
            del self.mPixmap
            self.mPixmap = QPixmap(self.size())
            self.mPixmap.fill(QColor(0, 0, 0, 0))
            painter = QPainter(self.mPixmap)
            self.draw_background(painter)
            self.mModified = False

        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.mPixmap)

    def draw_val(self):
        painter = QPainter(self)
        self.draw_value(painter)

    def paintEvent(self, event):

        if self.value_background:
            self.draw_val()
            self.draw_back()
        else:
            self.draw_back()
            self.draw_val()
