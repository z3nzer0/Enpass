import sys
from PyQt5.QtWidgets import QApplication

from GUILogin import GUILogin
from GUIMenu import GUIMenu
from GUIAccountCreate import GUIAccountCreate
from GUIAccountUpdate import GUIAccountUpdate

class GUIManager():

    core = None
    GUILogin = None
    GUIMenu = None
    GUIAccountCreate = None
    GUIAccountUpdate = None
    accountPage = None

    def __init__(self, core):
        self.core = core
        app = QApplication(sys.argv)
        self.GUILogin = GUILogin(self, self.core.checkFile(), self.core)
        sys.exit(app.exec_())

    def openMenu(self):
        self.GUILogin.close()
        self.GUIAccountCreate = GUIAccountCreate(self.core)
        self.GUIMenu = GUIMenu(self, self.core, self.GUIAccountCreate, self.GUIAccountUpdate)

    def updateAccountPage(self, account):
        if self.accountPage is not None:
          self.accountPage.close()
        self.accountPage = GUIAccountUpdate(account, self.core, self.GUIMenu)
        self.accountPage.show()


