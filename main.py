"""Main file of P-CHANGE application.

Build and launch the application.

"""

# Standard library imports
import logging

# Third party imports
from PySide2 import QtWidgets, QtGui

# Local application imports
from about_widget import About
from password_checker_widget import PasswordCheckerWidget
from password_generator_widget import PasswordGeneratorWidget


class PChangeApp(QtWidgets.QMainWindow):
    """
    A class to build the P-CHANGE application.

    Attributes
    ----------
    None

    Methods
    -------
    None

    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P-CHANGE (PasswordCHeckerANdGEnerator)")
        self.setWindowIcon(QtGui.QIcon("Lock-icon.png"))
        self.setFixedSize(400, 650)
        logging.basicConfig(level=logging.ERROR)
        tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(tab_widget)
        password_checker_widget = PasswordCheckerWidget()
        tab_widget.addTab(password_checker_widget, password_checker_widget.windowTitle())
        password_generator = PasswordGeneratorWidget()
        tab_widget.addTab(password_generator, password_generator.windowTitle())
        about_tab = About()
        tab_widget.addTab(about_tab, about_tab.windowTitle())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    pchange_app = PChangeApp()
    pchange_app.show()
    app.exec_()
