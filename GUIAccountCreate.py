from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption

class GUIAccountCreate(QWidget):

  core = None
  error = None

  def __init__(self, core):
    super().__init__()
    self.core = core
    self.setWindowTitle('Create Account')

    label1 = QLabel('Username/Email*',self)
    label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.usernameInput = QLineEdit(self)
    self.usernameInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.usernameInput.setAlignment(Qt.AlignCenter)

    label2 = QLabel('Password*',self)
    label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.passwordInput = QLineEdit(self)
    self.passwordInput.setEchoMode(QLineEdit.Password)
    self.passwordInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.passwordInput.setAlignment(Qt.AlignCenter)

    label3 = QLabel('Information',self)
    label3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.infoInput = QTextEdit(self)
    self.infoInput.setWordWrapMode(QTextOption.WrapAnywhere)
    self.infoInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.infoInput.setAlignment(Qt.AlignCenter)

    self.layout = QGridLayout()
    self.layout.addWidget(label1, 0, 0)
    self.layout.addWidget(self.usernameInput, 0, 1)

    self.layout.addWidget(label2, 1, 0)
    self.layout.addWidget(self.passwordInput, 1, 1)

    self.layout.addWidget(label3, 2, 0)
    self.layout.addWidget(self.infoInput, 2, 1)

    button=QPushButton('Add New',self)
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    button.clicked.connect(self.createAccount)

    self.layout.addWidget(button, 3, 0)

    self.setLayout(self.layout)
    self.show()

  def createAccount(self): 
    if len(self.usernameInput.text()) > 0 and len(self.passwordInput.text()) > 0:
      newUsername = self.usernameInput.text()
      newPassword = self.passwordInput.text()
      newInfo = self.infoInput.toPlainText()
      self.core.addNewAccount(newUsername, newPassword, newInfo)
      self.resetFields()
      self.error = QLabel('Account inserted successfully!',self)
      self.error.setStyleSheet("color: green")
      self.error.setAlignment(Qt.AlignCenter)
      self.layout.addWidget(self.error, 3, 1)
      self.setLayout(self.layout)
    else:
      self.error = QLabel('Fill all the required fields to CREATE the account!',self)
      self.error.setStyleSheet("color: red")
      self.error.setAlignment(Qt.AlignCenter)
      self.layout.addWidget(self.error, 3, 1)
      self.setLayout(self.layout)

  def resetFields(self):
    self.usernameInput.setText('')
    self.passwordInput.setText('')
    self.infoInput.setText('')
    if self.error is not None:
      self.error.setText('')