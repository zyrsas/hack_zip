#coding: utf8
import sys
import os
import time
import zipfile
import threading
import generate_word
import PyQt5.QtCore
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QFileDialog

app = QApplication(sys.argv)
app.setApplicationName('hack_rar')
form_class, base_class = loadUiType('window.ui')


class MainWindow(QDialog, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)

        self.setupUi(self)

        #zipFile for encoding
        self.zipFile = None
        #Type brute flag
        self.typeFlag = False
        #dictionary
        self.dict = None

        self.t = None
        self.flag = False
        #buttons connect with events
        self.btnOpen.clicked.connect(self.open_zip)
        self.btnOpenDict.clicked.connect(self.open_dict)
        self.btnStart.clicked.connect(self.brute_start)
        self.btnBust.clicked.connect(self.brute_bust)


    def open_zip(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', r"e:/Навчання/IV курс/II семестр/Безпека/hack_rar/")[0]
        self.edtPath.setText(str(fname))
        self.zipFile = zipfile.ZipFile(fname)

    def open_dict(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', r"e:/Навчання/IV курс/II семестр/Безпека/hack_rar/")[0]
        self.edtPathDict.setText(str(fname))
        self.dict = fname

    def brute_dict(self, password):
        try:
            self.txtStatus.append("Check: " + str(password))
            print(password)

            self.zipFile.extractall(pwd=password)
            self.txtStatus.append("[Successful] Password = " + str(password) + "\n")
            print("[Successful] Password = " + str(password) + "\n")
            self.flag = True

        except RuntimeError:
            pass
        except zipfile.BadZipfile:
            pass
        except Exception as e:
            pass

    def brute_start(self):
        self.txtStatus.append("Start...")
        with open(self.dict) as f:
                for line in f:
                    if self.flag:
                        return
                    password = line.strip("\n").encode()
                    self.t = threading.Thread(target=self.brute_dict, args=[password])
                    self.t.start()
                    time.sleep(0.00005)

    def brute_bust(self):
        self.txtStatus.append("Start...")
        UP_EN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        LOW_EN ='abcdefghijklmnopqrstuvwxyz'
        DIGITAL = '1234567890'
        SYMBOL = '~!@#$%^&*()_+=-`<>,./?;:\'"[]{}|\\'
        LIST = ''
        if self.chb_AZ.isChecked():
            LIST = LIST + UP_EN
        if self.chb_az.isChecked():
            LIST = LIST + LOW_EN
        if self.chb_09.isChecked():
            LIST = LIST + DIGITAL
        if self.chb_symb.isChecked():
            LIST = LIST + SYMBOL

        self.gen_usage(LIST)

    def gen_usage(self, LIST):
        length = int(self.edtLen.text())
        p = generate_word.EndsWithEngine(string_length=length, char_list=LIST)
        pwd = ''
        for password in p.generator():
            if self.flag:
                return
            pwd = ''.join(password)
            pwd = pwd.encode()
            self.t = threading.Thread(target=self.brute_dict, args=[pwd])
            self.t.start()
            time.sleep(0.00005)



#-----------------------------------------------------#
form = MainWindow()
form.setWindowTitle('hack_rar')
form.show()
sys.exit(app.exec_())