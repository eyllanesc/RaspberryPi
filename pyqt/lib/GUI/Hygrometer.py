# -*- coding: utf-8 -*-

import math
from PyQt5.QtCore import QObject, QSize, QPointF, Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QRadialGradient, QBrush, QPolygon, QFont, QPainterPath

from lib import AbstractMeter


class HygrometerPrivate(QObject):
    def __init__(self, q):
        QObject.__init__(self)
        self.mPointer = q

        self.mDigitFont = QFont()
        self.mDigitFont.setPointSizeF(18)

        self.mValueFont = QFont()
        self.mValueFont.setPointSizeF(22)

        self.mDigitOffset = 105.0

        self.mValueOffset = -100

    def draw_background(self, painter):
        self.initCoordinateSystem(painter)

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(4)
        painter.setPen(pen)

        back1 = QRadialGradient(QPointF(0.0, 0.0), 180.0, QPointF(-35.0, 145.0))
        back1.setColorAt(0.0, QColor(250, 250, 250))
        back1.setColorAt(1.0, QColor(20, 20, 20))

        back2 = QRadialGradient(QPointF(0.0, 0.0), 225.0, QPointF(76.5, 135.0))
        back2.setColorAt(0.0, QColor(10, 10, 10))
        back2.setColorAt(1.0, QColor(250, 250, 250))

        painter.setBrush(QBrush(back1))
        painter.drawEllipse(-162, -162, 324, 324);
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(back2))
        painter.drawEllipse(-152, -152, 304, 304)

        shield = QRadialGradient(QPointF(0, 0), 182, QPointF(-12.0, -15.0))
        shield.setColorAt(0.0, Qt.white)
        shield.setColorAt(0.5, QColor(240, 240, 240))
        shield.setColorAt(1.0, QColor(215, 215, 215))

        painter.setBrush(QBrush(shield))
        painter.setPen(pen)
        painter.drawEllipse(-142, -142, 284, 284)

        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(0, 200, 0))
        angle = int((3840 * (self.mPointer.nominal() - self.mPointer.minimal())) / (
            self.mPointer.maximal() - self.mPointer.minimal()))
        painter.drawPie(QRect(-141, -141, 282, 282), -480, 3840 - angle % 5760)

        painter.setBrush(QBrush(Qt.red))
        angle = int((3840 * (self.mPointer.critical() - self.mPointer.minimal())) / (
            self.mPointer.maximal() - self.mPointer.minimal()))
        painter.drawPie(QRect(-141, -141, 282, 282), -480, 3840 - angle % 5760)

        painter.setBrush(QBrush(shield))
        painter.drawEllipse(-129, -129, 258, 258)

        painter.rotate(60)

        painter.save()
        painter.setBrush(QBrush(Qt.black))
        line_length = 10
        scaleTriangle = [QPoint(-6, 141), QPoint(6, 141), QPoint(0, 129)]

        for i in range(33):
            painter.setPen(pen)
            if i % 4:
                painter.drawLine(0, 140, 0, 140 - line_length)
            else:
                painter.setPen(Qt.NoPen)
                painter.drawConvexPolygon(QPolygon(scaleTriangle))

            painter.rotate(7.5)
            pen.setWidth(3)

            if i % 2:
                line_length = 10
            else:
                line_length = 5

        painter.restore()

        painter.setPen(Qt.black)
        painter.rotate(-60.0)
        painter.setFont(self.mDigitFont)

        for i in range(9):
            v = self.mPointer.minimal() + i * (self.mPointer.maximal() - self.mPointer.minimal()) / 8.0
            if abs(v) < 0.000001:
                v = 0.0
            val = "{}".format(v)
            Size = painter.fontMetrics().size(Qt.TextSingleLine, val)
            painter.save()
            painter.translate(self.mDigitOffset * math.cos((5 + i) * math.pi / 6.0),
                              self.mDigitOffset * math.sin((5 + i) * math.pi / 6.0))
            painter.drawText(QPointF(Size.width() / -2.0, Size.height() / 4.0), val)
            painter.restore()

    def draw_value(self, painter):
        self.initCoordinateSystem(painter)
        hand = [-4, 0, -1, 129, 1, 129, 4, 0, 8, -50, -8, -50]

        hand_path = QPainterPath()
        hand_path.moveTo(QPointF(hand[0], hand[1]))

        for i in range(2, 10, 2):
            hand_path.lineTo(hand[i], hand[i + 1])

        hand_path.cubicTo(8.1, -51.0, 5.0, -48.0, 0.0, -48.0)
        hand_path.cubicTo(-5.0, -48.0, -8.1, -51.0, -8.0, -50.0)

        painter.save()

        painter.rotate(60.0)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.black))
        painter.rotate(((self.mPointer.value() -
                         self.mPointer.minimal()) * 240.0) / (self.mPointer.maximal() - self.mPointer.minimal()))

        painter.drawPath(hand_path)

        painter.drawEllipse(-10, -10, 20, 20)

        painter.restore()

        if self.mPointer.value() >= self.mPointer.critical():
            painter.setPen(Qt.red)

        painter.setFont(self.mValueFont)
        st = "{} %".format(self.mPointer.value())
        Size = painter.fontMetrics().size(Qt.TextSingleLine, st)
        painter.drawText(QPointF(Size.width() / -2, -self.mValueOffset), st)
        painter.end()

    def initCoordinateSystem(self, painter):
        side = min(self.mPointer.width(), self.mPointer.height())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.mPointer.width() / 2, self.mPointer.height() / 2)
        painter.scale(side / 335.0, side / 335.0)


class Hygrometer(AbstractMeter):
    def __init__(self, parent=None):
        AbstractMeter.__init__(self, parent=parent)
        self.dPtr = HygrometerPrivate(self)
        self.value_background = False

    def sizeHint(self):
        return QSize(300, 300)

    def draw_background(self, painter):
        self.dPtr.draw_background(painter)

    def draw_value(self, painter):
        self.dPtr.draw_value(painter)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Hygrometer()
    w.show()
    sys.exit(app.exec_())
