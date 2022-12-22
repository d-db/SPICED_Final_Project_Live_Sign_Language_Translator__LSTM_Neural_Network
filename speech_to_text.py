"""
Script to create a simple 'speech-to-text' translator within a GUI.
"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys
import speech_recognition as sr
import re


class MyWindow(QMainWindow):
    """
    Class to create the GUI for the 'speech-to-text' translator
    """

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(350, 350, 700, 200)
        self.setWindowTitle("Sprache-zu-Text Übersetzer")
        self._create_label()
        self._create_button_one()
        self._create_button_two()
        self.show()

    def _create_label(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Die Sprachaufnahme beginnt nach drücken des Buttons und\n"
                           "stoppt automatisch sobald Sie aufhören zu sprechen")
        self.label.move(50, 50)
        self.label.resize(600, 50)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(QFont('Times', 23))

    def _create_button_one(self):
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Aufnehmen")
        self.b1.clicked.connect(self._obtain_audio)
        self.b1.resize(150, 32)
        self.b1.move(50, 150)

    def _create_button_two(self):
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Beenden")
        self.b2.clicked.connect(self.close)
        self.b2.resize(150, 32)
        self.b2.move(500, 150)

    def _obtain_audio(self):
        print("Aufnahme wird gestartet")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        self._recognize_audio(audio)

        print("Aufnahme ist vorbei")

    def _recognize_audio(self, audio):
        print("recognition beginnt")
        r = sr.Recognizer()
        try:
            text = r.recognize_google(audio, language="de-DE")
        except sr.UnknownValueError:
            text = "Die Audioaufnahme konnte leider nicht ausgewertet werden."
        except sr.RequestError as e:
            text = f"Der folgende Fehler von Google Speech Recognition ist aufgetreten: {e}"

        # Break text after 10 whitespaces in order to display it properly within the window
        final_text = re.sub("((?:\S+\s){10}\S+)\s", "\\1\n", text, 0, re.DOTALL)

        print("recognition beendet")
        self.clicked(final_text)

    # Replace the initial text by the result of the 'speech-to-text' analysis!
    def clicked(self, text):
        self.label.setText(text)
        self.label.move(70, 50)
        self.update()

    def update(self):
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    app.exec()


if __name__ == "__main__":
    window()
