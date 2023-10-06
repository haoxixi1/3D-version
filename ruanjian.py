import os
import  time
import subprocess
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QLabel, QMessageBox
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QTimer, Qt, QThread, Signal
import PySide2
from qt_material import apply_stylesheet
from PySide2 import QtWidgets
from PySide2.QtGui import QFont



def handleCalc():
    try:
        time.sleep(3)
        # Start all timers
        timer.start(1)
        timer2.start(10)
        timer3.start(10)
    except Exception as e:
        QMessageBox.critical(window, "Error", str(e))

def updateTextEdit(output):
    textEdit3.appendPlainText(output)

def updateImage():
    pixmap = QPixmap("chuanshu/shipin.png")
    pixmap_resized = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
    imageLabel.setPixmap(pixmap_resized)

def updateImage2():
    pixmap = QPixmap("chuanshu/shendu.png")
    pixmap_resized = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
    imageLabel2.setPixmap(pixmap_resized)

def updateImage3():
    with open("chuanshu/output.txt", "r") as file:
        text = file.read()
    textEdit2.setPlainText(text)

# Set PySide2 plugin path
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

app = QApplication([])
app.setAttribute(Qt.AA_UseDesktopOpenGL)

font = QFont("Arial")
font.setPointSize(16)


window = QtWidgets.QMainWindow()
window.setWindowTitle('3D视觉')
window.setGeometry(100, 100, 1600, 1000)
apply_stylesheet(app, theme='dark_teal.xml')

imageLabel = QLabel(window)
imageLabel.move(100, 25)
imageLabel.resize(640, 480)

imageLabel2 = QLabel(window)
imageLabel2.move(100, 510)
imageLabel2.resize(640, 480)

textEdit2 = QPlainTextEdit(window)
textEdit2.move(1050, 25)
textEdit2.resize(500, 500)

textEdit3 = QPlainTextEdit(window)
textEdit3.setPlaceholderText("识别程序状态输出")
textEdit3.move(1060, 560)
textEdit3.resize(475, 300)
textEdit3.setFont(font)



button = QPushButton('开始', window)
button.move(1100, 880)
button.resize(200, 100)
button.clicked.connect(handleCalc)

timer = QTimer()
timer.timeout.connect(updateImage)

timer2 = QTimer()
timer2.timeout.connect(updateImage2)


timer3 = QTimer()
timer3.timeout.connect(updateImage3)



window.show()
app.exec_()