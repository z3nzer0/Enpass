import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt

class GUILogin(QWidget):

  GUIManager = None
  core = None
  error = None

  def __init__(self, GUIManager, isLogin, core):
    super().__init__()
    self.GUIManager = GUIManager
    self.core = core
    self.left = 600
    self.top = 350
    if isLogin:
      self.Login()
    else:
      self.setPassword()

  def checkFirstPass(self):
    if self.error : 
      self.layout.removeWidget(self.error)

    if self.inputPass1.text() != self.inputPass2.text():
      self.error = QLabel('Passwords does not match!',self)
    elif self.core.masterPassRegex(self.inputPass1.text()) is None:
      self.error = QLabel('Passwords need to be at least 12 characters long and contains upper/lower letters, numbers and special characters!',self)
    else:
      self.core.setMasterPass(self.inputPass1.text())
      self.GUIManager.openMenu()

    if self.error :
      self.error.setStyleSheet("color: red")
      self.error.setWordWrap(True)
      self.error.setAlignment(Qt.AlignCenter)

      self.layout.addWidget(self.error, 5, 0)
      self.setLayout(self.layout)

  def checkMasterPass(self):
    if self.core.checkMasterPass(self.masterPass.text()):
      self.GUIManager.openMenu()
    else:
      self.error = QLabel('Wrong Passwords!',self)

    if self.error :
      self.error.setStyleSheet("color: red")
      self.error.setWordWrap(True)
      self.error.setAlignment(Qt.AlignCenter)
      self.layout.addWidget(self.error, 3, 0)
      self.setLayout(self.layout)

  def setPassword(self):
    self.setWindowTitle('Set Password')
    self.setGeometry(self.left,self.top,0,0)
    self.setFixedSize(350,250)

    label1 = QLabel('Password',self)
    label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    label2 = QLabel('Repeat Password',self)
    label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.inputPass1 = QLineEdit(self)
    self.inputPass1.setEchoMode(QLineEdit.Password)
    self.inputPass1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.inputPass1.setAlignment(Qt.AlignCenter)

    self.inputPass2 = QLineEdit(self)
    self.inputPass2.setEchoMode(QLineEdit.Password)
    self.inputPass2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.inputPass2.setAlignment(Qt.AlignCenter)

    button=QPushButton('Set Password',self)
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    button.clicked.connect(self.checkFirstPass)

    self.layout = QGridLayout()
    self.layout.addWidget(label1, 0, 0)
    self.layout.addWidget(self.inputPass1, 1, 0)
    self.layout.addWidget(label2, 2, 0)
    self.layout.addWidget(self.inputPass2, 3, 0)
    self.layout.addWidget(button, 4, 0)

    self.setLayout(self.layout)
    self.show()

  def Login(self):
    self.setWindowTitle('Login')
    self.setGeometry(self.left,self.top,300,200)
    self.setFixedSize(300,200)

    label = QLabel('Password',self)
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    label.setAlignment(Qt.AlignCenter)

    self.masterPass = QLineEdit(self)
    self.masterPass.setEchoMode(QLineEdit.Password)
    self.masterPass.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.masterPass.setAlignment(Qt.AlignCenter)

    button=QPushButton('Login',self)
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    button.clicked.connect(self.checkMasterPass)

    self.layout = QGridLayout()
    self.layout.addWidget(label, 0, 0)
    self.layout.addWidget(self.masterPass, 1, 0)
    self.layout.addWidget(button, 2, 0)

    self.setLayout(self.layout)
    self.show()