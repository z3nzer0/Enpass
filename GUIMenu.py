import sys, pyperclip
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QSizePolicy, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption

GUIManager = None
core = None
mainWindow = None
GUIAccountCreate = None
GUIAccountUpdate = None

class GUIMenu(QMainWindow):

  def __init__(self, GUIM, core, GUIAC, GUIAU):
    super().__init__()
    global mainWindow, GUIAccountCreate, GUIAccountUpdate, GUIManager
    mainWindow = self
    GUIAccountCreate = GUIAC
    GUIAccountUpdate = GUIAU
    GUIManager = GUIM
    self.core = core
    self.title='Menu'
    self.left=600
    self.top=350
    self.width=850
    self.height=500
    self.initUI()

  def initUI(self):
    self.setWindowTitle(self.title)
    self.setGeometry(self.left,self.top,self.width,self.height)
    self.tab_widget = TabWidget(self, self.core) 
    self.setCentralWidget(self.tab_widget)
    self.show()

  def updateTable(self):
    self.tab_widget.deleteLater()
    self.tab_widget = TabWidget(self, self.core)
    self.setCentralWidget(self.tab_widget)
    self.show()
    

class TabWidget(QTabWidget):

  core = None
  menu = None
  table = None
  createWindow = None

  def __init__(self, parent, core): 
    super(QWidget, self).__init__(parent)
    self.core = core
    self.menu = parent
    self.layout = QVBoxLayout(self) 

    
    self.tab1 = QWidget()
    self.tab2 = QWidget()
    self.resize(300, 200) 

    
    self.addTab(self.tab1, "Credentials") 
    self.addTab(self.tab2, "Add New Credential") 

    
    self.tab1.layout = QVBoxLayout() 
    self.table = TableWithButtons(self.core, self.menu)
    self.tab1.layout.addWidget(self.table) 
    self.tab1.setLayout(self.tab1.layout)

    global GUIAccountCreate
    
    self.tab2.layout = QVBoxLayout()
    self.createWindow = GUIAccountCreate
    self.tab2.layout.addWidget(self.createWindow)
    self.tab2.setLayout(self.tab2.layout)

    
    self.layout.addWidget(self) 
    self.setLayout(self.layout)

    self.currentChanged.connect(self.onTabChanged)

  def onTabChanged(self, index):
    if index == 1:
      self.createWindow.resetFields()
    elif index == 0:
      global mainWindow
      mainWindow.updateTable()

class TableWithButtons(QWidget):

  core = None
  menu = None

  def __init__(self, core, menu):
    self.core = core
    self.menu = menu
    super().__init__()

    ### ACCOUNTS TAB ###
    data = self.core.getDecodedData()

    
    self.table = QTableWidget(len(data['accounts']), 4)
    self.table.verticalHeader().setDefaultSectionSize(60)
    self.table.horizontalHeader().setDefaultSectionSize(170)
    self.table.setColumnWidth(3, 250)
    self.table.verticalHeader().hide()

    self.table.setWordWrap(True)
    
    columnText = ['Username/Email', 'Information', 'Password', 'Actions']
    for col in range(4):
      self.table.setHorizontalHeaderItem(col, QTableWidgetItem(f""+columnText[col]))

    for row in range(len(data['accounts'])):
      tempLabel = QLabel(data['accounts'][row]['username'],self)
      tempLabel.setAlignment(Qt.AlignCenter)
      self.table.setCellWidget(row, 0, tempLabel)

    
      info_textbox = QTextEdit(self)
      info_textbox.setPlainText(data['accounts'][row]['info'])
      info_textbox.setFixedHeight(60)
      info_textbox.setStyleSheet("padding: 5px;")
      info_textbox.setReadOnly(True) 
      self.table.setCellWidget(row, 1, info_textbox)


      tempLabel = QLabel('************',self)
      tempLabel.setAlignment(Qt.AlignCenter)
      self.table.setCellWidget(row, 2, tempLabel)

      container_widget = QWidget()
      layout = QHBoxLayout()

      global GUIManager

      
      buttonModify=QPushButton('Modify',self)
      buttonModify.clicked.connect(lambda ch, account = data['accounts'][row]: GUIManager.updateAccountPage(account))
      buttonModify.setStyleSheet("background-color: #ffa502")

      buttonCopy=QPushButton('Copy',self)
      buttonCopy.clicked.connect(lambda ch, password = data['accounts'][row]['password']: self.copyPassword(password))
      buttonCopy.setStyleSheet("background-color: #2ed573")

      buttonRemove=QPushButton('Remove',self)
      buttonRemove.clicked.connect(lambda ch, accountID = data['accounts'][row]['id']: self.confirmRemove(accountID))
      buttonRemove.setStyleSheet("background-color: #FF0000")

      
      layout.addWidget(buttonModify)
      layout.addWidget(buttonCopy)
      layout.addWidget(buttonRemove)

      
      container_widget.setLayout(layout)

      self.table.setCellWidget(row, 3, container_widget)

    self.table.resizeRowsToContents()
    self.table.horizontalHeader().setStretchLastSection(True)

    
    layout = QVBoxLayout()
    layout.addWidget(self.table)
    self.setLayout(layout)
    self.show()

  def copyPassword(self, password):
    pyperclip.copy(password)

  def confirmRemove(self, id):
    reply = QMessageBox.question(self,"Confirm Action","Are you sure you want to delete this account?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
    if reply == QMessageBox.Yes:  
      self.removeAccount(id)

  def removeAccount(self, id):
    global mainWindow
    self.core.removeAccount(id)
    mainWindow.updateTable()