"""Widget 'Password Checker' which is one tab of P-CHANGE application.

Define a widget that allows the user to check whether the provided password has already been exposed in data
breaches or not.

Classes
-------
PasswordCheckerWidget
"""

# Third party imports
from PySide2 import QtWidgets, QtCore, QtGui
from qtwidgets import PasswordEdit

# Local application imports
from password_checker import PasswordChecker


class PasswordCheckerWidget(QtWidgets.QWidget):
    """
    A class to have a widget that allows to check a given password.

    Attributes
    ----------
    pwd_checker : PasswordChecker
        the object that can perform the password checking
    line_edit_password : PasswordEdit
        line edit widget that allows the user to enter a password
    button_check : QtWidgets.QPushButton
        button widget that allows the user to launch the password checking
    plain_text_edit_results : QtWidgets.QPlainTextEdit
        plain text edit widget that is used to display the results of the password checking
    """

    def __init__(self):
        """
        Perform all the initializations and build the widget.
        """

        super().__init__()
        self.setWindowTitle("Password Checker")
        self.__build_widget()
        self.__setup_connections()
        self._pwd_checker = PasswordChecker()

    def __build_widget(self):
        """
        Build the widget.
        """

        # Group Box "Input"
        group_box_input = QtWidgets.QGroupBox("Input")
        layout_input = QtWidgets.QVBoxLayout()
        self._line_edit_password = PasswordEdit()
        layout_input.addWidget(self._line_edit_password)
        group_box_input.setLayout(layout_input)

        # Button "CHECK"
        self._button_check = QtWidgets.QPushButton("CHECK")
        self._button_check.setIcon(QtGui.QIcon(QtGui.QPixmap("Lock-icon.png")))
        self._button_check.setFixedSize(100, 30)

        # Group Box "Results"
        group_box_results = QtWidgets.QGroupBox("Results")
        group_box_results.setFixedHeight(200)
        layout_results = QtWidgets.QVBoxLayout()
        self._plain_text_edit_results = QtWidgets.QPlainTextEdit()
        self._plain_text_edit_results.setReadOnly(True)
        self._plain_text_edit_results.setStyleSheet("""QPlainTextEdit
                                                       {background-color: #D8DEE4;
                                                        color: #333;
                                                        font: bold 11px;
                                                        font-family: Verdana;}""")
        layout_results.addWidget(self._plain_text_edit_results)
        group_box_results.setLayout(layout_results)

        # dummy Group Box
        # TODO: remove this dummy zone and learn how to actually place all the widgets
        group_box_dummy = QtWidgets.QGroupBox("")
        group_box_dummy.setFlat(True)
        group_box_dummy.setFixedHeight(400)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(group_box_input)
        main_layout.addWidget(self._button_check, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(group_box_results)
        main_layout.addWidget(group_box_dummy)

    def __setup_connections(self):
        """
        Setup the connections between a user action on the widget and the method to execute.
        """

        self._button_check.clicked.connect(self.__check)
        self._line_edit_password.returnPressed.connect(self.__check)

    def __check(self):
        """
        Perform the password check and display the result.
        """
        self._pwd_checker.password = self._line_edit_password.text()
        self._pwd_checker.has_to_be_hidden = not self._line_edit_password.password_shown
        self._plain_text_edit_results.setPlainText(self._pwd_checker.check())
        self._line_edit_password.setText("")
