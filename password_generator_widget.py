"""Widget 'Password Generator' which is one tab of P-CHANGE application.

Define a widget that allows the user to get a new password satisfying each rule he has selected.

Classes
-------
PasswordCheckerWidget
"""

# Standard library imports
from email.message import EmailMessage
import smtplib

# Third party imports
from PySide2 import QtWidgets, QtCore, QtGui

# Local application imports
from password_generator import PasswordGenerator, PasswordRules, PasswordRuleError


class PasswordGeneratorWidget(QtWidgets.QWidget):
    """
    A class to have a widget that allows to generate a password satisfying rules.

    Attributes
    ----------
    pwd_generator : PasswordGenerator
        the object that can perform the password generation
    spin_box_chars_min : QtWidgets.QSpinBox
        spin box widget that allows the user to select the minimum number of characters in the password
    spin_box_chars_max : QtWidgets.QSpinBox
        spin box widget that allows the user to select the maximum number of characters in the password
    line_edit_special_chars : QtWidgets.QLineEdit
        line edit widget that allows the user to enter the special characters authorized in the password
    check_box_lower_case_letter : QtWidgets.QCheckBox
        check box widget that allows the user to select the lower case letter presence rule
    check_box_upper_case_letter : QtWidgets.QCheckBox
        check box widget that allows the user to select the upper case letter presence rule
    check_box_number : QtWidgets.QCheckBox
        check box widget that allows the user to select the number presence rule
    check_box_special_char : QtWidgets.QCheckBox
        check box widget that allows the user to select the special character presence rule
    line_edit_first_chars : QtWidgets.QLineEdit
        line edit widget that allows the user to enter the desired first characters in the password
    line_edit_last_chars : QtWidgets.QLineEdit
        line edit widget that allows the user to enter the desired last characters in the password
    group_box_send_mail : QtWidgets.QGroupBox
        group box widget that allows the user to specify that the results must be sent by email
    line_edit_email : QtWidgets.QLineEdit
        line edit widget that allows the user to enter his email address
    button_generate : QtWidgets.QPushButton
        button widget that allows the user to launch the password generation
    plain_text_edit_results : QtWidgets.QPlainTextEdit
        plain text edit widget that is used to display the results of the password generation
    """

    def __init__(self):
        """
        Perform all the initializations and build the widget.
        """
        super().__init__()
        self.setWindowTitle("Password Generator")
        self.__build_widget()
        self.__setup_connections()
        self._pwd_generator = PasswordGenerator()

    def __build_widget(self):
        """
        Build the widget.
        """

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.__build_group_box_rules())
        main_layout.addWidget(self.__build_group_box_customization())
        self.__build_group_box_email()
        main_layout.addWidget(self._group_box_send_mail)
        self.__build_button_generate()
        main_layout.addWidget(self._button_generate, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.__build_group_box_results())

    def __build_group_box_rules(self):
        """
        Build the group box widget that contains all the rules.

        Returns
        -------
        QtWidgets.QGroupBox
            The group box containing all rules.
        """

        # GroupBox and Layout for rules
        group_box_rules = QtWidgets.QGroupBox("Rules")
        layout_rules = QtWidgets.QVBoxLayout()

        layout_rules.addWidget(self.__build_group_box_size_rules())
        layout_rules.addWidget(self.__build_group_box_special_characters_rule())
        layout_rules.addWidget(self.__build_group_box_presence_rules())

        group_box_rules.setLayout(layout_rules)

        return group_box_rules

    def __build_group_box_size_rules(self):
        """
        Build the group box widget that contains the size rules.

        Returns
        -------
        QtWidgets.QGroupBox
            The group box containing all size rules.
        """

        # GroupBox and Layout for size rules
        group_box_size_rules = QtWidgets.QGroupBox("Size")
        layout_size_rules = QtWidgets.QGridLayout()

        # Layout for min nb of chars
        label_chars_min = QtWidgets.QLabel("Min number of chars")
        self._spin_box_chars_min = QtWidgets.QSpinBox()
        self._spin_box_chars_min.setRange(1, 100)
        self._spin_box_chars_min.setFixedSize(50, 20)
        self._spin_box_chars_min.setAlignment(QtCore.Qt.AlignRight)
        layout_size_rules.addWidget(label_chars_min, 0, 0)
        layout_size_rules.addWidget(self._spin_box_chars_min, 0, 1)

        # Layout for max nb of chars
        label_chars_max = QtWidgets.QLabel("Max number of chars")
        self._spin_box_chars_max = QtWidgets.QSpinBox()
        self._spin_box_chars_max.setRange(1, 100)
        self._spin_box_chars_max.setFixedSize(50, 20)
        self._spin_box_chars_max.setAlignment(QtCore.Qt.AlignRight)
        layout_size_rules.addWidget(label_chars_max, 1, 0)
        layout_size_rules.addWidget(self._spin_box_chars_max, 1, 1)

        group_box_size_rules.setLayout(layout_size_rules)
        return group_box_size_rules

    def __build_group_box_special_characters_rule(self):
        """
        Build the group box widget that contains the special characters rule.

        Returns
        -------
        QtWidgets.QGroupBox
            The group box containing the special character rule.
        """

        # GroupBox and Layout for special characters rule
        group_box_special_characters_rule = QtWidgets.QGroupBox("Special characters")
        layout_special_characters_rule = QtWidgets.QGridLayout()

        # Layout for special chars
        label_special_chars = QtWidgets.QLabel("Allowed special chars")
        self._line_edit_special_chars = QtWidgets.QLineEdit()
        self._line_edit_special_chars.setAlignment(QtCore.Qt.AlignRight)
        self._line_edit_special_chars.setClearButtonEnabled(True)
        self._line_edit_special_chars.setFixedSize(200, 20)
        layout_special_characters_rule.addWidget(label_special_chars, 0, 0)
        layout_special_characters_rule.addWidget(self._line_edit_special_chars, 0, 1)

        group_box_special_characters_rule.setLayout(layout_special_characters_rule)

        return group_box_special_characters_rule

    def __build_group_box_presence_rules(self):
        """
        Build the group box widget that contains the presence rules.

        Returns
        -------
        QtWidgets.QGroupBox
            The group box containing all presence rules.
        """

        # GroupBox and Layout for presence rules
        group_box_presence_rules = QtWidgets.QGroupBox("Presence")
        group_box_presence_rules.setToolTip("At least 1 presence rule must be selected !")
        layout_presence_rules = QtWidgets.QGridLayout()

        # Layout for lower case letter
        label_lower_case_letter = QtWidgets.QLabel("At least 1 lower case letter")
        self._check_box_lower_case_letter = QtWidgets.QCheckBox()
        self._check_box_lower_case_letter.setFixedSize(20, 20)
        layout_presence_rules.addWidget(label_lower_case_letter, 0, 0)
        layout_presence_rules.addWidget(self._check_box_lower_case_letter, 0, 1, QtCore.Qt.AlignRight)

        # Layout for upper case letter
        label_upper_case_letter = QtWidgets.QLabel("At least 1 upper case letter")
        self._check_box_upper_case_letter = QtWidgets.QCheckBox()
        self._check_box_upper_case_letter.setFixedSize(20, 20)
        layout_presence_rules.addWidget(label_upper_case_letter, 1, 0)
        layout_presence_rules.addWidget(self._check_box_upper_case_letter, 1, 1, QtCore.Qt.AlignRight)

        # Layout for number
        label_number = QtWidgets.QLabel("At least 1 number")
        self._check_box_number = QtWidgets.QCheckBox()
        self._check_box_number.setFixedSize(20, 20)
        layout_presence_rules.addWidget(label_number, 2, 0)
        layout_presence_rules.addWidget(self._check_box_number, 2, 1, QtCore.Qt.AlignRight)

        # Layout for special char
        label_special_char = QtWidgets.QLabel("At least 1 special char")
        self._check_box_special_char = QtWidgets.QCheckBox()
        self._check_box_special_char.setFixedSize(20, 20)
        layout_presence_rules.addWidget(label_special_char, 3, 0)
        layout_presence_rules.addWidget(self._check_box_special_char, 3, 1, QtCore.Qt.AlignRight)

        group_box_presence_rules.setLayout(layout_presence_rules)

        return group_box_presence_rules

    def __build_group_box_customization(self):
        """
        Build the group box widget that contains the customization option.

        Returns
        -------
        QtWidgets.QGroupBox
            The group box containing the customization options.
        """

        # GroupBox and Layout for optional customization
        group_box_optional_customization = QtWidgets.QGroupBox("Optional customization")
        layout_optional_customization = QtWidgets.QGridLayout()

        # Layout for first chars
        label_first_chars = QtWidgets.QLabel("First chars")
        self._line_edit_first_chars = QtWidgets.QLineEdit()
        layout_optional_customization.addWidget(label_first_chars, 0, 0)
        layout_optional_customization.addWidget(self._line_edit_first_chars, 0, 1)

        # Layout for last chars
        label_last_chars = QtWidgets.QLabel("Last chars")
        self._line_edit_last_chars = QtWidgets.QLineEdit()
        layout_optional_customization.addWidget(label_last_chars, 1, 0)
        layout_optional_customization.addWidget(self._line_edit_last_chars, 1, 1)

        group_box_optional_customization.setLayout(layout_optional_customization)

        return group_box_optional_customization

    def __build_group_box_email(self):
        """
        Build the group box widget that contains the email option.
        """

        # GroupBox and Layout for mail option
        self._group_box_send_mail = QtWidgets.QGroupBox("Send results by email")
        self._group_box_send_mail.setCheckable(True)
        self._group_box_send_mail.setChecked(False)

        # Disabled for now...
        self._group_box_send_mail.setDisabled(True)
        self._group_box_send_mail.setToolTip("Disabled for now. Sorry")

        layout_mail = QtWidgets.QGridLayout()
        label_mail = QtWidgets.QLabel("Email")
        self._line_edit_email = QtWidgets.QLineEdit()
        layout_mail.addWidget(label_mail, 0, 0)
        layout_mail.addWidget(self._line_edit_email, 0, 1)
        self._group_box_send_mail.setLayout(layout_mail)

    def __build_button_generate(self):
        """
        Build the button that allows to launch the password generation.
        """

        # Button "GENERATE"
        self._button_generate = QtWidgets.QPushButton("GENERATE")
        self._button_generate.setIcon(QtGui.QIcon(QtGui.QPixmap("Lock-icon.png")))
        self._button_generate.setFixedSize(150, 30)

    def __build_group_box_results(self):
        """
        Build the group box widget that contains the results.

        Returns
        -------
        QtWidgets.QGroupBox
            The group box containing the results zone.
        """

        # GroupBox and Layout for results
        group_box_results = QtWidgets.QGroupBox("Results")
        group_box_results.setFixedHeight(100)
        layout_results = QtWidgets.QHBoxLayout()
        self._plain_text_edit_results = QtWidgets.QPlainTextEdit()
        self._plain_text_edit_results.setReadOnly(True)
        self._plain_text_edit_results.setStyleSheet("""QPlainTextEdit
                                                        {background-color: #D8DEE4;
                                                         color: #333;
                                                         font: bold 11px;
                                                         font-family: Verdana;}""")
        layout_results.addWidget(self._plain_text_edit_results)
        group_box_results.setLayout(layout_results)

        return group_box_results

    def __setup_connections(self):
        """
        Setup the connections between a user action on the widget and the method to execute.
        """
        self._button_generate.clicked.connect(self.__generate)

    def __send_password_by_email(self, password):
        """
        Send the provided password to the email address filled by the user.

        Parameters
        ----------
        password : str
            The password to send.
        """

        # I know this is NOT secure, it's just a temporary feature to see if I'm able to do that !
        email = EmailMessage()
        email["From"] = "P-CHANGE"
        email["To"] = self._line_edit_email.text()
        # TO DO : check email address validity
        email["Subject"] = "P-CHANGE result"
        email.set_content(password)

        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login("python-pchange@gmail.com", "Python33!")

                smtp.send_message(email)
            except (smtplib.SMTPAuthenticationError,
                    smtplib.SMTPRecipientsRefused,
                    smtplib.SMTPHeloError,
                    smtplib.SMTPSenderRefused,
                    smtplib.SMTPDataError,
                    smtplib.SMTPNotSupportedError,
                    smtplib.SMTPException) as err:
                self._plain_text_edit_results.setPlainText(f"SMTP error : {err}")
            else:
                self._plain_text_edit_results.setPlainText(
                    f"The generated password has successfully been sent to {self._line_edit_email.text()}")
            finally:
                smtp.quit()

    def __generate(self):
        """
        Retrieve all the rules and options selected by the user then generate a consistent password.
        """

        # Retrieve the rules values
        rules = PasswordRules()
        rules.min_number_of_chars = self._spin_box_chars_min.value()
        rules.max_number_of_chars = self._spin_box_chars_max.value()
        rules.allowed_special_characters = [char for char in self._line_edit_special_chars.text()]
        rules.set_presence_rules(self._check_box_lower_case_letter.isChecked(),
                                 self._check_box_upper_case_letter.isChecked(),
                                 self._check_box_number.isChecked(),
                                 self._check_box_special_char.isChecked())
        # Retrieve the customized strings
        rules.set_customized_strings(self._line_edit_first_chars.text(), self._line_edit_last_chars.text())

        self._pwd_generator._rules = rules

        # Generate the new password and display it
        try:
            generated_password = self._pwd_generator.generate()
        except PasswordRuleError as e:
            self._plain_text_edit_results.setPlainText(f"The following error occurred :\n{e}")
        else:
            if self._group_box_send_mail.isChecked():
                self._send_password_by_email(generated_password)
            else:
                self._plain_text_edit_results.setPlainText(f"The generated password is :\n'{generated_password}'")
