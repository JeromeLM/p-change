"""Widget 'About' which is one tab of P-CHANGE application.

Give some information about the application, the current release and the contributors.

Classes
-------
About
"""

# Third party imports
from PySide2 import QtWidgets, QtCore


class About(QtWidgets.QWidget):
    """
    A class to have a widget that displays information about the application.
    """

    def __init__(self):
        """
        Perform all the initializations and build the widget.
        """
        super().__init__()
        self.setWindowTitle("About")
        self.__build_widget()

    def __build_widget(self):
        """
        Build the widget.
        """

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # Summary
        group_box_summary = QtWidgets.QGroupBox("Summary")
        layout_summary = QtWidgets.QVBoxLayout()
        plain_text_summary = QtWidgets.QPlainTextEdit()
        plain_text_summary.setReadOnly(True)
        plain_text_summary.setStyleSheet("""QPlainTextEdit
                                            {background-color: #D8DEE4;
                                             color: #333;
                                             font: bold 11px;
                                             font-family: Verdana;}""")
        plain_text_summary.setPlainText("This tool provides two features :\n\n"
                                        "- password checking : it retrieves info from https://haveibeenpwned.com/ "
                                        "and informs the user whether his password has already been exposed in data "
                                        "breaches or not\n\n"
                                        "- password generation : it provides a random password satisfying each "
                                        "rule selected by the user\n\n"
                                        "Initially, I created this tool while following the amazing course "
                                        "'Complete Python Developer in 2020: Zero to Mastery' by Andrei Neagoie, "
                                        "to put into practice some of the things I was learning.\nPlease be "
                                        "indulgent as this is my first tool developed in Python and Qt.\n"
                                        "Constructive feedback is welcome and you can even ask to contribute "
                                        "if you want to.\n\nThanks,\nJerome Lapeyre-Mirande")
        layout_summary.addWidget(plain_text_summary)
        group_box_summary.setLayout(layout_summary)

        # Release
        group_box_release = QtWidgets.QGroupBox("Release")
        main_layout_release = QtWidgets.QGridLayout()
        label_id_text = QtWidgets.QLabel("Identifier")
        label_id_value = QtWidgets.QLabel("1.0")
        main_layout_release.addWidget(label_id_text, 0, 0)
        main_layout_release.addWidget(label_id_value, 0, 1, alignment=QtCore.Qt.AlignRight)
        label_date_text = QtWidgets.QLabel("Date")
        label_date_value = QtWidgets.QLabel("06/04/2020")
        main_layout_release.addWidget(label_date_text, 1, 0)
        main_layout_release.addWidget(label_date_value, 1, 1, alignment=QtCore.Qt.AlignRight)
        group_box_release.setLayout(main_layout_release)

        # Author
        group_box_author = self.__build_group_box_person("Author", False, "Jerome Lapeyre-Mirande", "TBD",
                                                         "https://www.linkedin.com/in/jlapeyremirande/",
                                                         "linkedin")

        # Contributors
        group_box_contributors = QtWidgets.QGroupBox("Contributors")
        main_layout_contributors = QtWidgets.QVBoxLayout()

        group_box_contributor1 = self.__build_group_box_person("", True, "John Doe", "john.doe.fake@gmail.com",
                                                               "https://www.linkedin.com",
                                                               "linkedin")
        main_layout_contributors.addWidget(group_box_contributor1)

        group_box_contributor2 = self.__build_group_box_person("", True, "Jess Doe", "jess.doe.fake@mail.com",
                                                               "https://github.com/",
                                                               "github")
        main_layout_contributors.addWidget(group_box_contributor2)

        group_box_contributors.setLayout(main_layout_contributors)

        # Main layout
        main_layout.addWidget(group_box_summary)
        main_layout.addWidget(group_box_release)
        main_layout.addWidget(group_box_author)
        main_layout.addWidget(group_box_contributors)

    def __build_group_box_person(self, group_name="", is_flat=False, name="John Doe",
                                 email="TBD", link="TBD", link_desc="TBD"):
        """
        Build a group box containing information about one person.

        Parameters
        ----------
        group_name : str
            The name of the group box (default is "")
        is_flat : bool
            An indicator whether the group box must be flat or not (default is False)
        name : str
            The name of the person (default is "")
        email : str
            The email address of the person (default is "TBD")
        link : str
            A link to a website the person wants to share (default is "TBD")
        link_desc : str
            A simple description of the web link (default is "TBD")

        Returns
        -------
        QtWidgets.QGroupBox
            The group box containing all the person's information.
        """

        group_box = QtWidgets.QGroupBox(group_name)
        if is_flat: group_box.setFlat(True)

        layout = QtWidgets.QGridLayout()
        label_name_text = QtWidgets.QLabel("Name")
        label_name_value = QtWidgets.QLabel(name)
        layout.addWidget(label_name_text, 0, 0)
        layout.addWidget(label_name_value, 0, 1, alignment=QtCore.Qt.AlignRight)
        label_mail_text = QtWidgets.QLabel("Mail")
        label_mail_value = QtWidgets.QLabel(email)
        layout.addWidget(label_mail_text, 1, 0)
        layout.addWidget(label_mail_value, 1, 1, alignment=QtCore.Qt.AlignRight)
        label_link_text = QtWidgets.QLabel("Link")
        label_link_value = QtWidgets.QLabel(f"<a href='{link}'>{link_desc}</a>")
        label_link_value.setOpenExternalLinks(True)
        layout.addWidget(label_link_text, 2, 0)
        layout.addWidget(label_link_value, 2, 1, alignment=QtCore.Qt.AlignRight)
        group_box.setLayout(layout)

        return group_box
