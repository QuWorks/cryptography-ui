import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5 import uic


class MainApp(QMainWindow, QWidget):
    def __init__(self, text):
        super().__init__()
        uic.loadUi("msgbox.xml", self)  # ui file load

        self.textinmsgbox = text
        self.labeltext.setText(self.textinmsgbox)

        self.btn_ok.clicked.connect(self.quit)

    def quit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp("test")
    appMain.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exiting...')
