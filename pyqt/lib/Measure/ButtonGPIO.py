# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFormLayout

from lib import Switch


class GroupButtonGPIO(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.layout = QFormLayout(self)

    def addButton(self, pin, name):
        m = GPIO.getmode()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)
        s = Switch()
        self.layout.addRow(name, s)
        s.clicked.connect(lambda checked, p=pin: self.onOff(checked, p))
        if m:
            GPIO.setmode(m)

    @pyqtSlot(bool, name='onOff')
    def onOff(self, checked, p):
        GPIO.output(p, checked)

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()
