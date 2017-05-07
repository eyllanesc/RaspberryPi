# -*- coding: utf-8 -*-

import Adafruit_DHT
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, qApp

from lib import Thermometer, Hygrometer


class ThermometerThread(QThread):
    finished = pyqtSignal()
    changedValue = pyqtSignal(float, float)
    mRunning = True

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        while self.mRunning:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
            self.changedValue.emit(humidity, temperature)
            qApp.processEvents()
            self.sleep(1)
        self.finished.emit()

    def stopWork(self):
        self.mRunning = False


class DHTGPIO(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QHBoxLayout(self)

        self.h = Hygrometer(self)
        self.t = Thermometer(self)

        lay.addWidget(self.h)
        lay.addWidget(self.t)

        self.thread = ThermometerThread()
        self.thread.changedValue.connect(self.setValue)
        self.thread.start()

    def setValue(self, humidity, temperature):
        self.h.setValue(humidity)
        self.t.setValue(temperature)

    def __del__(self):
        self.thread.quit()
        self.thread.wait()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QWidget
    import sys

    app = QApplication(sys.argv)
    w = DHTGPIO()
    w.show()
    sys.exit(app.exec_())
