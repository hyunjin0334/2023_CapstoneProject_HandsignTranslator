from PyQt5 import QtCore, QtGui, QtWidgets
import os


class Ui_PsyBer(object):
    def setupUi(self, PsyBer):
        PsyBer.setObjectName("PsyBer")
        PsyBer.resize(1300, 900)
        self.centralwidget = QtWidgets.QWidget(PsyBer)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 1300, 900))
        font = QtGui.QFont()
        font.setPointSize(90)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(480, 50, 391, 171))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(80)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.funinf = QtWidgets.QPushButton(self.centralwidget)
        self.funinf.setGeometry(QtCore.QRect(750, 320, 400, 460))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.funinf.setFont(font)
        self.funinf.setObjectName("funinf")

        self.funstt = QtWidgets.QPushButton(self.centralwidget)
        self.funstt.setGeometry(QtCore.QRect(150, 320, 400, 460))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.funstt.setFont(font)
        self.funstt.setObjectName("funstt")
        PsyBer.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(PsyBer)
        self.statusbar.setObjectName("statusbar")
        PsyBer.setStatusBar(self.statusbar)
        
        self.fundic = QtWidgets.QPushButton(self.centralwidget)
        self.fundic.setGeometry(QtCore.QRect(1150, 20, 120, 70))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(15)
        font.setBold(True)
        self.fundic.setFont(font)
        self.fundic.setObjectName("dictionary")
        
        self.retranslateUi(PsyBer)
        QtCore.QMetaObject.connectSlotsByName(PsyBer)

    def translate_to_sign_language(self):
        os.system("python app/stt_to_sign.py")

    def translate_to_korean(self):
        os.system("python app/sign_to_korean.py")

    def dictionary(self):
        os.system("python app/sign_dictionary.py")

    def retranslateUi(self, PsyBer):
        _translate = QtCore.QCoreApplication.translate
        PsyBer.setWindowTitle(_translate("PsyBer", "PsyBer"))
        self.label.setText(_translate("PsyBer", "PsyBer"))
        self.funstt.setText(_translate("PsyBer", "한국어를 수어로!"))
        self.funinf.setText(_translate("PsyBer", "수어를 한국어로!"))
        self.fundic.setText(_translate("PsyBer", "수어 사전"))
        
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PsyBer = QtWidgets.QMainWindow()
    ui = Ui_PsyBer()
    ui.setupUi(PsyBer)

    #"한국어를 수어로"
    ui.funstt.clicked.connect(ui.translate_to_sign_language)

    # "수어를 한국어로" 
    ui.funinf.clicked.connect(ui.translate_to_korean)

    # "수어 사전" 
    ui.fundic.clicked.connect(ui.dictionary)

    PsyBer.show()
    sys.exit(app.exec_())