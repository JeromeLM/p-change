"""Generator of password used by the 'Password Generator' tab of P-CHANGE application.

Define classes that allow to specify password rules and to generate a new password.

Classes
-------
Error
PasswordRuleError
PasswordRules
PasswordGenerator
"""

# Standard library imports
import logging
import random
import string


class Error(Exception):
    pass


class PasswordRuleError(Error):
    def __init__(self, message):
        self.message = message


class PasswordRules:
    """
    A class to define rules to be satisfied when creating a password.

    Attributes
    ----------
    min_number_of_chars : int
        the minimum number of characters to be contained in the password
    max_number_of_chars : int
        the maximum number of characters to be contained in the password
    allowed_special_characters : list
        the list of special characters that can be contained in the password
    is_lower_case_required : bool
        an indicator whether at least 1 lower case letter has to be contained or not in the password
    is_upper_case_required : bool
        an indicator whether at least 1 upper case letter has to be contained or not in the password
    is_number_required : bool
        an indicator whether at least 1 number has to be contained or not in the password
    is_special_character_required : bool
        an indicator whether at least 1 special character has to be contained or not in the password
    customized_beginning : str
        a string that allows to customize the password's first characters
    customized_end : str
        a string that allows to customize the password's last characters
    length_of_customized_beginning : int
        the length of the customized beginning string
    length_of_customized_end : str
        the length of the customized end string

    Methods
    -------
    min_number_of_chars():
        Return the minimum number of characters.
    min_number_of_chars(new_value):
        Set the 'min_number_of_chars' attribute to the provided value.
    max_number_of_chars():
        Return the maximum number of characters.
    max_number_of_chars(new_value):
        Set the 'max_number_of_chars' attribute to the provided value.
    allowed_special_characters():
        Return the list of special characters.
    allowed_special_characters(new_values):
        Set the 'allowed_special_characters' attribute to the provided values.
    is_lower_case_required():
        Return True if at least 1 lower case letter has to be contained in the password, False otherwise
    is_lower_case_required(new_value):
        Set the 'is_lower_case_required' attribute to the provided value.
    is_upper_case_required():
        Return True if at least 1 upper case letter has to be contained in the password, False otherwise
    is_upper_case_required(new_value):
        Set the 'is_upper_case_required' attribute to the provided value.
    is_number_required():
        Return True if at least 1 number has to be contained in the password, False otherwise
    is_number_required(new_value):
        Set the 'is_number_required' attribute to the provided value.
    is_special_character_required():
        Return True if at least 1 special character has to be contained in the password, False otherwise
    is_special_character_required(new_value):
        Set the 'is_special_character_required' attribute to the provided value.
    set_presence_rules(lower_case=False, upper_case=False, number=False, special_character=False):
        Set all the presence rules ('is_lower_case_required', 'is_upper_case_required', 'is_number_required' and
        'is_special_character_required') to the provided values.
    customized_beginning():
        Return the customized first characters of the password.
    customized_beginning(new_value):
        Set the 'customized_beginning' attribute to the provided value. Update 'length_of_customized_beginning'.
    customized_end():
        Return the customized last characters of the password.
    customized_end(new_value):
        Set the 'customized_end' attribute to the provided value. Update 'length_of_customized_end'.
    length_of_customized_beginning():
        Return the length of the customized first characters of the password.
    length_of_customized_end():
        Return the length of the customized last characters of the password.
    set_customized_strings(beginning, end):
        Set the 'customized_beginning' and 'customized_end' attributes to the provided values.
        Update the associated length attributes.
    get_nb_of_presence_rules():
        Return the number of presence rules that are actually selected.
    get_nb_of_rules_satisfied_by_string(string_to_check):
        Return the number of presence rules satisfied by the string passed in.
    is_lower_case_rule_satisfied(string_to_check):
        Return True if the provided string satisfies the lower case rule, False otherwise.
    is_upper_case_rule_satisfied(string_to_check):
        Return True if the provided string satisfies the upper case rule, False otherwise.
    is_number_rule_satisfied(string_to_check):
        Return True if the provided string satisfies the number rule, False otherwise.
    is_special_character_rule_satisfied(string_to_check):
        Return True if the provided string satisfies the special character rule, False otherwise.
    check_rules_consistency():
        Check the consistency between all the rules.
        Return consistency status and reason of inconsistency.
    """

    def __init__(self):
        """
        Initialize all the necessary attributes with default values.
        """

        self._min_number_of_chars = 1
        self._max_number_of_chars = 1
        self._allowed_special_characters = []
        self._is_lower_case_required = False
        self._is_upper_case_required = False
        self._is_number_required = False
        self._is_special_character_required = False
        self._customized_beginning = ""
        self._customized_end = ""
        self._length_of_customized_beginning = 0
        self._length_of_customized_end = 0

    def __str__(self):
        return (f"- min number of chars = {self._min_number_of_chars}\n"
                f"- max number of chars = {self._max_number_of_chars}\n"
                f"- allowed special characters = {' '.join(self._allowed_special_characters)}\n"
                f"- is lower case required = {self._is_lower_case_required}\n"
                f"- is upper case required = {self._is_upper_case_required}\n"
                f"- is number required = {self._is_number_required}\n"
                f"- is special character required = {self._is_special_character_required}\n"
                f"- length of customized beginning = {self._length_of_customized_beginning}\n"
                f"- length of customized end = {self._length_of_customized_end}\n"
                f"- customized beginning = '{self._customized_beginning}'\n"
                f"- customized end = '{self._customized_end}'\n")

    # Getters and setters
    # ===================

    @property
    def min_number_of_chars(self):
        return self._min_number_of_chars

    @min_number_of_chars.setter
    def min_number_of_chars(self, new_value):
        if new_value > 0 and isinstance(new_value, int):
            self._min_number_of_chars = new_value
        else:
            raise ValueError("Set a valid integer value > 1 for attribute 'min_number_of_chars'")

    @property
    def max_number_of_chars(self):
        return self._max_number_of_chars

    @max_number_of_chars.setter
    def max_number_of_chars(self, new_value):
        if new_value > 0 and isinstance(new_value, int):
            self._max_number_of_chars = new_value
        else:
            raise ValueError("Set a valid integer value > 1 for attribute 'max_number_of_chars'")

    @property
    def allowed_special_characters(self):
        return self._allowed_special_characters

    @allowed_special_characters.setter
    def allowed_special_characters(self, new_values):
        if isinstance(new_values, list):
            if all([isinstance(item, str) for item in new_values]):
                self._allowed_special_characters = new_values[:]
            else:
                raise ValueError("Set a valid list of str for attribute 'allowed_special_characters'")
        else:
            raise ValueError("Set a valid list of str for attribute 'allowed_special_characters'")

    @property
    def is_lower_case_required(self):
        return self._is_lower_case_required

    @is_lower_case_required.setter
    def is_lower_case_required(self, new_value):
        if isinstance(new_value, bool):
            self._is_lower_case_required = new_value
        else:
            raise ValueError("Set a bool value for attribute 'is_lower_case_required'")

    @property
    def is_upper_case_required(self):
        return self._is_upper_case_required

    @is_upper_case_required.setter
    def is_upper_case_required(self, new_value):
        if isinstance(new_value, bool):
            self._is_upper_case_required = new_value
        else:
            raise ValueError("Set a bool value for attribute 'is_upper_case_required'")

    @property
    def is_number_required(self):
        return self._is_number_required

    @is_number_required.setter
    def is_number_required(self, new_value):
        if isinstance(new_value, bool):
            self._is_number_required = new_value
        else:
            raise ValueError("Set a bool value for attribute 'is_number_required'")

    @property
    def is_special_character_required(self):
        return self._is_special_character_required

    @is_special_character_required.setter
    def is_special_character_required(self, new_value):
        if isinstance(new_value, bool):
            self._is_special_character_required = new_value
        else:
            raise ValueError("Set a bool value for attribute 'is_special_character_required'")

    @property
    def customized_beginning(self):
        return self._customized_beginning

    @customized_beginning.setter
    def customized_beginning(self, new_value):
        if isinstance(new_value, str):
            self._customized_beginning = new_value
            self._length_of_customized_beginning = len(new_value)
        else:
            raise ValueError("Set a str value for attribute 'customized_beginning'")

    @property
    def customized_end(self):
        return self._customized_end

    @customized_end.setter
    def customized_end(self, new_value):
        if isinstance(new_value, str):
            self._customized_end = new_value
            self._length_of_customized_end = len(new_value)
        else:
            raise ValueError("Set a str value for attribute 'customized_end'")

    @property
    def length_of_customized_beginning(self):
        return self._length_of_customized_beginning

    @property
    def length_of_customized_end(self):
        return self._length_of_customized_end

    # "Public" methods
    # ================

    def set_presence_rules(self, lower_case=False, upper_case=False, number=False, special_character=False):
        """
        Set the presence rules attributes to the provided values.

        Parameters
        ----------
        lower_case : bool, optional
            The value of the presence rule 'is_lower_case_required' (default is False)
        upper_case : bool, optional
            The value of the presence rule 'is_upper_case_required' (default is False)
        number : bool, optional
            The value of the presence rule 'is_number_case_required' (default is False)
        special_character : bool, optional
            The value of the presence rule 'is_special_character_required' (default is False)
        """

        self._is_lower_case_required = lower_case
        self._is_upper_case_required = upper_case
        self._is_number_required = number
        self._is_special_character_required = special_character

    def set_customized_strings(self, beginning="", end=""):
        """
        Set the customized strings (first characters and last characters) attributes to the provided values.
        Update the associated length attributes.

        Parameters
        ----------
        beginning : str
            The value of the customized first characters (default is "")
        end : str
            The value of the customized last characters (default is "")
        """

        self._customized_beginning = beginning
        self._customized_end = end
        self._length_of_customized_beginning = len(beginning)
        self._length_of_customized_end = len(end)

    def get_nb_of_presence_rules(self):
        """
        Return the number of presence rules that are selected.

        Returns
        -------
        int
            The number of selected presence rules.
        """

        return sum([
            self._is_lower_case_required,
            self._is_upper_case_required,
            self._is_number_required,
            self._is_special_character_required
        ])

    def get_nb_of_rules_satisfied_by_string(self, string_to_check):
        """
        Return the number of presence rules satisfied by the provided string.

        Parameters
        ----------
        string_to_check : str
            The string to evaluate.

        Returns
        -------
        int
            The number of satisfied presence rules.
        """

        nb_of_satisfied_rules = 0
        if self._is_lower_case_required and self.is_lower_case_rule_satisfied(string_to_check):
            nb_of_satisfied_rules += 1
        if self._is_upper_case_required and self.is_upper_case_rule_satisfied(string_to_check):
            nb_of_satisfied_rules += 1
        if self._is_number_required and self.is_number_rule_satisfied(string_to_check):
            nb_of_satisfied_rules += 1
        if self._is_special_character_required and self.is_special_character_rule_satisfied(string_to_check):
            nb_of_satisfied_rules += 1
        return nb_of_satisfied_rules

    def is_lower_case_rule_satisfied(self, string_to_check):
        """
        Return True if the lower case rule is satisfied by the provided string, False otherwise.

        Parameters
        ----------
        string_to_check : str
            The string to evaluate.

        Returns
        -------
        bool
            An indicator whether the lower case rule is satisfied or not.
        """

        return any([char.islower() for char in string_to_check])

    def is_upper_case_rule_satisfied(self, string_to_check):
        """
        Return True if the upper case rule is satisfied by the provided string, False otherwise.

        Parameters
        ----------
        string_to_check : str
            The string to evaluate.

        Returns
        -------
        bool
            An indicator whether the upper case rule is satisfied or not.
        """
        return any([char.isupper() for char in string_to_check])

    def is_number_rule_satisfied(self, string_to_check):
        """
        Return True if the number case rule is satisfied by the provided string, False otherwise.

        Parameters
        ----------
        string_to_check : str
            The string to evaluate.

        Returns
        -------
        bool
            An indicator whether the number case rule is satisfied or not.
        """
        return any([char.isdigit() for char in string_to_check])

    def is_special_character_rule_satisfied(self, string_to_check):
        """
        Return True if the special character case rule is satisfied by the provided string, False otherwise.

        Parameters
        ----------
        string_to_check : str
            The string to evaluate.

        Returns
        -------
        bool
            An indicator whether the special character case rule is satisfied or not.
        """
        return any([char in self._allowed_special_characters for char in string_to_check])

    def check_rules_consistency(self):
        """
        Check the consistency between all the rules.

        Returns
        -------
        tuple
            Boolean indicator of consistency, String reason of inconsistency
        """

        nb_of_presence_rules = self.get_nb_of_presence_rules()

        # Ensure at least one presence rule is required
        if nb_of_presence_rules == 0:
            inconsistency_reason = "At least one presence rule must be selected"
            return False, inconsistency_reason

        # Ensure length of customized strings are consistent with other size rules
        # and ensure customized strings satisfy presence rules
        if self._length_of_customized_beginning + self._length_of_customized_end > self._max_number_of_chars:
            if self._length_of_customized_beginning > self._max_number_of_chars:
                inconsistency_reason = f"The number of customized first chars cannot be greater " \
                                       f"than 'max number of chars'"
            elif self._length_of_customized_end > self._max_number_of_chars:
                inconsistency_reason = "The number of customized last chars cannot be greater " \
                                       "than 'max number of chars'"
            else:
                inconsistency_reason = "The total number of customized chars cannot be greater " \
                                       "than 'max number of chars'"
            return False, inconsistency_reason

        if self._length_of_customized_beginning > 0 \
                and not self.__check_string_consistency(self._customized_beginning):
            inconsistency_reason = "The customized first chars are not consistent with at least one rule"
            return False, inconsistency_reason

        if self._length_of_customized_end > 0 and not self.__check_string_consistency(self._customized_end):
            inconsistency_reason = "The customized last chars are not consistent with at least one rule"
            return False, inconsistency_reason

        # Ensure "min number of chars" is lower or equal to "max number of chars"
        if self._min_number_of_chars > self._max_number_of_chars:
            inconsistency_reason = "'min number of chars' cannot be greater than 'max number of chars'"
            return False, inconsistency_reason

        # Ensure all the presence rules can be satisfied
        if nb_of_presence_rules > self._min_number_of_chars:
            if not self._customized_beginning and not self._customized_end:
                inconsistency_reason = "All presence rules cannot be satisfied with current 'min nb of chars'"
                return False, inconsistency_reason
            else:
                # Determine how many rules are satisfied by customized strings
                nb_of_satisfied_rules = self.get_nb_of_rules_satisfied_by_string(self._customized_beginning
                                                                                 + self._customized_end)
                if nb_of_satisfied_rules < nb_of_presence_rules:
                    # Check if there are enough chars left (max - len(customized strings)) for unsatisfied rules
                    if (self._max_number_of_chars - len(self._customized_beginning + self._customized_end)) \
                        < (nb_of_presence_rules - nb_of_satisfied_rules):
                        inconsistency_reason = "All presence rules cannot be satisfied with current settings " \
                                               "('max_nb_of_chars', customized beginning and customized end)"
                        return False, inconsistency_reason

        # if "special character" rule is required, ensure there is at least one special character defined
        if self.is_special_character_required and not self.allowed_special_characters:
            inconsistency_reason = "'special character' rule selected but no special character provided"
            return False, inconsistency_reason

        return True, ""

    # "Private" methods
    # =================

    def __check_string_consistency(self, string_to_check):
        """
        Determine if at least one rule is broken by the string passed in.

        Parameters
        ----------
        string_to_check : str
            The string to evaluate.

        Returns
        -------
        bool
            An indicator whether the string is consistent with all the rules or not.
        """

        if not self._is_lower_case_required and any([char.islower() for char in string_to_check]):
            logging.error(f"At least one unexpected lower case letter in {string_to_check}")
            return False
        if not self._is_upper_case_required and any([char.isupper() for char in string_to_check]):
            logging.error(f"At least one unexpected upper case letter in {string_to_check}")
            return False
        if not self._is_number_required and any([char.isdigit() for char in string_to_check]):
            logging.error(f"At least one unexpected number in {string_to_check}")
            return False
        if not self._is_special_character_required:
            if any([not char.isdigit() and not char.isalpha() for char in string_to_check]):
                logging.error(f"At least one unexpected special character in {string_to_check}")
                return False
        # TODO : improve with regexp ?
        elif any([char not in self._allowed_special_characters and not char.isdigit() and not char.isalpha() for char in
                  string_to_check]):
            logging.error(f"At least one not allowed special character in {string_to_check}")
            return False

        return True


class PasswordGenerator:
    """
    A class to generate a password, satisfying all the rules.

    Attributes
    ----------
    rules : PasswordRules
        the rules that the generated password must satisfy.

    Methods
    -------
    rules():
        Return the rules to satisfy.
    rules(rules):
        Set the 'rules' attribute to the provided value.
    generate():
        Return a password satisfying all the rules.
    """

    def __init__(self):

        """
        Initialize all the attributes with default values.
        """
        self._rules = PasswordRules()

    # Getters and setters
    # ===================

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules):
        if isinstance(rules, PasswordRules):
            self._rules = rules
        else:
            raise ValueError("Set a valid PasswordRules value for attribute 'rules'")

    # "Public" methods
    # ================

    def generate(self):
        """
        Generate a password satisfying each rule.

        Returns
        -------
        str
            The generated password.

        Raises
        ------
        PasswordRuleError
            If the rules are not consistent
        """

        # At first, check the consistency between all rules
        are_rules_consistent, inconsistency_reason = self._rules.check_rules_consistency()
        if not are_rules_consistent:
            raise PasswordRuleError(inconsistency_reason)

        rules_states = {
            # <rule name>: [<is it required ?>, <is it satisfied ?>]
            "lower case": [self._rules.is_lower_case_required, False],
            "upper case": [self._rules.is_upper_case_required, False],
            "number": [self._rules.is_number_required, False],
            "special character": [self._rules.is_special_character_required, False]
        }

        # Determine how many rules are still to satisfy after taking into account the customized strings
        if self._rules.length_of_customized_beginning > 0 or self._rules.length_of_customized_end > 0:
            customized_string = self._rules.customized_beginning + self._rules.customized_end
            nb_of_satisfied_rules = self._rules.get_nb_of_rules_satisfied_by_string(customized_string)
            nb_of_unsatisfied_rules = self._rules.get_nb_of_presence_rules() - nb_of_satisfied_rules
            if nb_of_satisfied_rules > 0:
                if rules_states["lower case"][0]:
                    rules_states["lower case"][1] = self._rules.is_lower_case_rule_satisfied(customized_string)
                if rules_states["upper case"][0]:
                    rules_states["upper case"][1] = self._rules.is_upper_case_rule_satisfied(customized_string)
                if rules_states["number"][0]:
                    rules_states["number"][1] = self._rules.is_number_rule_satisfied(customized_string)
                if rules_states["special character"][0]:
                    rules_states["special character"][1] = self._rules.is_special_character_rule_satisfied(
                        customized_string)
        else:
            nb_of_unsatisfied_rules = self._rules.get_nb_of_presence_rules()

        password = self._rules.customized_beginning

        # Satisfy each remaining unsatisfied rule
        for i in range(nb_of_unsatisfied_rules):
            if rules_states["lower case"][0] and not rules_states["lower case"][1]:
                password += random.choice(string.ascii_lowercase)
                rules_states["lower case"][1] = True

            elif rules_states["upper case"][0] and not rules_states["upper case"][1]:
                password += random.choice(string.ascii_uppercase)
                rules_states["upper case"][1] = True

            elif rules_states["number"][0] and not rules_states["number"][1]:
                password += str(random.randint(0, 9))
                rules_states["number"][1] = True

            elif rules_states["special character"][0] and not rules_states["special character"][1]:
                password += random.choice(self._rules.allowed_special_characters)
                rules_states["special character"][1] = True

            else:
                break

        # At this stage all the rules are satisfied
        # Now, simply complete the password with a random number of additional characters (if necessary)
        additional_chars = []
        additional_chars += list(string.ascii_lowercase) if self._rules.is_lower_case_required else []
        additional_chars += list(string.ascii_uppercase) if self._rules.is_upper_case_required else []
        additional_chars += list(string.digits) if self._rules.is_number_required else []
        additional_chars += self._rules.allowed_special_characters if self._rules.is_special_character_required else []
        nb_of_chars_left = self._rules.max_number_of_chars - len(password) - self._rules.length_of_customized_end
        if nb_of_chars_left > 0:
            for i in range(random.randrange(1, nb_of_chars_left + 1, 1)):
                password += random.choice(additional_chars)

        # Ensure there will be at least 'min_nb_of_chars' characters in the password
        # (It can happen due to the random.randrange() used above)
        if (len(password) + self._rules.length_of_customized_end) < self._rules.min_number_of_chars:
            for i in range(self._rules.min_number_of_chars - (len(password) + self._rules.length_of_customized_end)):
                password += random.choice(additional_chars)

        # Don't forget to add the customized end if required
        if self._rules.length_of_customized_end > 0:
            password += self._rules.customized_end

        return password
