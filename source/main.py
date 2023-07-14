from cryptography import fernet
import easygui
import threading
import shutil
import pydlli

import msgbox

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon

fern = pydlli.import_dll("fernet.dll")
shutil.rmtree("temp/")


def _browse():
    i = easygui.fileopenbox("Open file", "Open file")
    if i == "" or i is None:
        return None
    return i


def _elements_manage(elementlist, enabled: bool):
    i = enabled
    for item in elementlist:
        item.setEnabled(i)


class MainApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("window.xml", self)  # ui file load
        # self.setWindowIcon(QIcon("PATH_ICON"))  # Icon Loading
        self.crypt_mode = 0

        self.interact_list = [
            self.line_file,
            self.line_key,
            self.browse_file,
            self.browse_key,
            self.btn_enc,
            self.btn_dec,
            self.btn_gen
        ]

        self.btn_gen.clicked.connect(self.generate_key)
        self.browse_file.clicked.connect(self.browsefile)
        self.browse_key.clicked.connect(self.browsekey)

        self.btn_enc.clicked.connect(self.button_encrypt)
        self.btn_dec.clicked.connect(self.button_decrypt)

    def _msgbox(self, text):
        self.box = msgbox.MainApp(text)
        self.box.show()

    def generate_key(self):
        i = fernet.Fernet.generate_key()
        if not os.path.exists('keys/'):
            os.mkdir('keys/')

        open('keys/_generatedKey.cryptography', 'wb').write(i)

    def browsefile(self):
        path = _browse()
        if path is None:
            print(': Browse cancelled')
        else:
            self.line_file.setText(str(path))

    def browsekey(self):
        path = _browse()
        if path is None:
            print(': Browse cancelled')
        else:
            self.line_key.setText(str(path))

    def button_encrypt(self):
        self.crypt_mode = 1
        self.check_before_crypt()

    def button_decrypt(self):
        self.crypt_mode = 2
        self.check_before_crypt()

    def check_before_crypt(self):
        # Set variables
        filepath = self.line_file.text()
        keypath = self.line_key.text()
        #

        # Check if key & file exists
        if not os.path.exists(filepath):
            print(': File doesnt exist!')
            self._msgbox("File doesnt exist")
            return _elements_manage(self.interact_list, True)

        if not os.path.exists(keypath):
            print(': Key doesnt exist!')
            self._msgbox("Key doesnt exist")
            return _elements_manage(self.interact_list, True)

        filecontent = open(filepath, 'rb').read()
        keycontent = open(keypath, 'rb').read()

        x = threading.Thread(target=self.crypt)
        x.start()

    def crypt(self):
        _elements_manage(self.interact_list, False)

        filepath = self.line_file.text()
        keypath = self.line_key.text()
        file_content = open(filepath, 'rb').read()
        key = open(keypath, 'rb').read()

        try:
            if self.crypt_mode == 1:  # If encrypt
                crypted = fern["Encrypt"](key, file_content)
            elif self.crypt_mode == 2:  # If decrypted
                crypted = fern["Decrypt"](key, file_content)
            else:
                print(': self.crypt_mode is 0...')
                return _elements_manage(self.interact_list, True)
        except fernet.InvalidToken:
            print(': Invalid cryptography key')
            return _elements_manage(self.interact_list, True)

        open(filepath, 'wb').write(crypted)  # Writing to file

        print(': Finished')
        _elements_manage(self.interact_list, True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp()
    appMain.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exiting...')
