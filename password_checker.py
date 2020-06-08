"""Checker of password used by the 'Password Checker' tab of P-CHANGE application.

Define one class that allows to retrieve from 'haveibeenpwned.com' whether the current password has already been
exposed in data breaches or not.

Classes
-------
PasswordChecker
"""

# Standard library imports
import hashlib
import re

# Third party imports
import requests


class PasswordChecker:
    """
    A class to check a password.

    Attributes
    ----------
    password : str
        the password to check
    has_to_be_hidden : bool
        an indicator whether the password has to be hidden or not when returning check result

    Methods
    -------
    password():
        Return the password to check.
    password(new_value):
        Set the 'password' attribute to the provided value.
    has_to_be_hidden():
        Return True if the password has to be hidden in results.
    has_to_be_hidden(new_value):
        Set the 'has_to_be_hidden' attribute to the provided value.
    check():
        Check whether the current password has already been exposed in data breaches or not.
    """

    def __init__(self, password="", has_to_be_hidden=True):
        """
        Initialize all the necessary attributes with the provided or default values.

        Parameters
        ----------
        password : str (default = "")
            Password to be checked.
        has_to_be_hidden : bool (default = True)
            Indicator whether the password has to be hidden or not in the check results.
        """

        self._password = password
        self._has_to_be_hidden = has_to_be_hidden

    def __str__(self):
        if self._has_to_be_hidden:
            pwd = ''.join(re.sub('.', '*', self._password))
        else:
            pwd = self._password
        return (f"password = {pwd}\n"
                f"has_to_be_hidden = {self._has_to_be_hidden}")

    # Getters and setters
    # ===================

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_value):
        if isinstance(new_value, str):
            self._password = new_value
        else:
            raise ValueError(f"Bad type provided for 'password' member. Expected {type(self._password)}, "
                             f"received {type(new_value)}")

    @property
    def has_to_be_hidden(self):
        return self._has_to_be_hidden

    @has_to_be_hidden.setter
    def has_to_be_hidden(self, new_value):
        if isinstance(new_value, bool):
            self._has_to_be_hidden = new_value
        else:
            raise ValueError(f"Bad type provided for 'has_to_be_hidden' member. "
                             f"Expected {type(self._has_to_be_hidden)}, received {type(new_value)}")

    # "Public" methods
    # ================

    def check(self):
        """
        Check whether the current password has already been exposed in data breaches or not.

        Returns
        -------
        str
            A string with the result and the associated advice.
        """
        if self._password:
            count = self.__pwned_api_check(self._password)
            password_string = self._password if not self._has_to_be_hidden else "This password"
            if count:
                return f"{password_string} has already been exposed in data breaches ({count} times) : you should " \
                       f"probably change it !!"
            else:
                return f"{password_string} has never been exposed in data breaches : you can keep it :-)"
        return "Empty password provided. No reason to check it !"

    # "Private" methods
    # =================

    def __request_api_data(self, url):
        """
        Using the provided url, get the response of the API.

        Parameters
        ----------
        url : str
            The url of the API to use.

        Raises
        ------
        RuntimeError
            If the status code received in the response is different from 200.
        """

        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f"Error fetching : response status code = {response.status_code}, "
                               f"check the API and try again")
        return response

    def __get_pwd_leaks_count(self, hashes, hashed_pwd_tail):
        """
        From the provided list of hashed password' tails and associated count, return the count of the hashed password's
        tail passed in.

        Parameters
        ----------
        hashes : requests.models.Response
            Object containing all the hashed password' tails and associated count.
        hashed_pwd_tail:
            Hashed password's tail to search for.
        """

        hashes = (line.split(':') for line in hashes.text.splitlines())
        for tail, count in hashes:
            if tail == hashed_pwd_tail:
                return count
        return 0

    def __pwned_api_check(self, password):
        """
        Use the API provided by https://api.pwnedpasswords.com/range/ to know whether the given password has already
        been exposed or not.

        To avoid any security issue, the given password is not provided as is to the API.
        It's firstly hashed then only the first 5 characters are provided.

        Parameters
        ----------
        password : str
            Password to check.

        Returns
        -------
        int
            The number of times the password has been exposed in data breaches.
        """

        # Hash the given password then retrieve the first 5 characters and the remaining characters called the tail.
        sha1_pwd = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        first_5_chars, tail = sha1_pwd[:5], sha1_pwd[5:]

        # response is : the tail of each password that matches the first 5 chars, followed by the number of times
        # it has been exposed
        # tail:3
        # tail:53
        # ...
        url = "https://api.pwnedpasswords.com/range/" + first_5_chars
        try:
            response = self.__request_api_data(url)
        except RuntimeError as e:
            return f"Failed to get the information ({e})"
        else:
            return self.__get_pwd_leaks_count(response, tail)
