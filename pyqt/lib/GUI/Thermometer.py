# -*- coding: utf-8 -*-

from PyQt5.QtCore import QPointF, Qt, QObject, QRectF, QSize
from PyQt5.QtGui import QPainter, QPainterPath, QLinearGradient, QGradient, QColor, QBrush, QPen, QRadialGradient, \
    QFont
from PyQt5.QtWidgets import QApplication

from lib import AbstractMeter


class ThermometerPrivate(QObject):
    def __init__(self, q):
        QObject.__init__(self)
        self.mPointer = q

        self.mDigitFont = QFont()
        self.mDigitFont.setPointSizeF(8)

        self.mValueFont = QFont()
        self.mValueFont.setPointSizeF(8)

    def draw_background(self, painter):

        self.initCoordinateSystem(painter)

        glass = QPainterPath()
        glass.moveTo(12.5, 267.5)
        glass.quadTo(12.5, 263.0, 7.5, 257.0)

        glass.lineTo(7.5, 25.0)
        glass.quadTo(7.5, 12.5, 0, 12.5)
        glass.quadTo(-7.5, 12.5, -7.5, 25.0)
        glass.lineTo(-7.5, 257.0)

        glass.quadTo(-12.5, 263.0, -12.5, 267.5)
        glass.quadTo(-12.5, 278.0, 0.0, 280.0)
        glass.quadTo(12.5, 278.0, 12.5, 267.5)

        linearGrad = QLinearGradient(QPointF(-2.0, 0.0), QPointF(12.5, 0.0))
        linearGrad.setSpread(QGradient.ReflectSpread)
        linearGrad.setColorAt(1.0, QColor(0, 150, 255, 170))
        linearGrad.setColorAt(0.0, QColor(255, 255, 255, 0))

        painter.setBrush(QBrush(linearGrad))
        painter.setPen(Qt.black)
        painter.drawPath(glass)

        pen = QPen()

        for i in range(33):
            pen.setWidthF(1.0)
            length = 12
            if i % 4:
                length = 8
                pen.setWidthF(0.75)
            if i % 2:
                length = 5
                pen.setWidthF(0.5)

            painter.setPen(pen)
            painter.drawLine(-7, 28 + 7*i, -7 + length, 28 + 7*i)

        painter.setFont(self.mDigitFont)
        for i in range(9):
            val = self.mPointer.minimal() + i * (self.mPointer.maximal() - self.mPointer.minimal()) / 8.0
            Size = painter.fontMetrics().size(Qt.TextSingleLine, str(val))
            painter.drawText(QPointF(10, 252 - i * 28 + Size.width() / 4.0), str(val))

    def draw_value(self, painter):

        self.initCoordinateSystem(painter)

        color = QColor(Qt.blue)
        if self.mPointer.value() >= self.mPointer.nominal():
            color = QColor(0, 200, 0)
        if self.mPointer.value() >= self.mPointer.critical():
            color = QColor(Qt.red)

        factor = (self.mPointer.value() - self.mPointer.minimal()) / (self.mPointer.maximal() - self.mPointer.minimal())

        painter.setFont(self.mValueFont)
        st = "{} ℃".format(self.mPointer.value())
        Size = painter.fontMetrics().size(Qt.TextSingleLine, st)
        painter.drawText(QPointF(Size.width() / -2, 307-Size.height()), st)

        slug = QLinearGradient(0.0, 0.0, 5.0, 0.0)
        tank = QRadialGradient(0.0, 267.0, 10.0, -5.0, 262.0)

        slug.setSpread(QGradient.ReflectSpread)
        tank.setSpread(QGradient.ReflectSpread)

        color.setHsv(color.hue(), color.saturation(), color.value())
        slug.setColorAt(1.0, color)
        tank.setColorAt(1.0, color)

        color.setHsv(color.hue(), color.saturation() - 200, color.value())
        slug.setColorAt(0.0, color)
        tank.setColorAt(0.0, color)

        painter.setPen(Qt.NoPen)
        painter.setBrush(slug)

        offset = 10

        temp = 224*factor

        height = temp + offset

        if 231 < temp:
            height = 231 + offset
        if offset - 5 >= height:
            height = offset-5

        painter.drawRect(-5, 252 + offset - height, 10, height)

        painter.setBrush(tank)
        painter.drawEllipse(QRectF(-10.0, 257.5, 20.0, 20.0))

        painter.end()

    def initCoordinateSystem(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.mPointer.width() / 2.0, 0.0)
        painter.scale(self.mPointer.height() / 300.0, self.mPointer.height() / 307.0)


class Thermometer(AbstractMeter):
    def __init__(self, parent=None):
        AbstractMeter.__init__(self, parent=parent)
        self.dPtr = ThermometerPrivate(self)

    def sizeHint(self):
        return QSize(300, 300)

    def draw_background(self, painter):
        self.dPtr.draw_background(painter)

    def draw_value(self, painter):
        self.dPtr.draw_value(painter)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Thermometer()
    w.show()
    sys.exit(app.exec_())
