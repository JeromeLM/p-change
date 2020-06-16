# p-change
Password CHecker ANd GEnerator application built in python.

This tool provides two features :
- password checking : it retrieves info from https://haveibeenpwned.com/ and informs the user whether his password has already been exposed in data breaches or not
- password generation : it provides a random password satisfying each rule selected by the user

Initially, I created this tool while following the amazing course 'Complete Python Developer in 2020: Zero to Mastery' by Andrei Neagoie, to put into practice some of the things I was learning.
Please be indulgent as this is my first tool developed in Python and Qt.
Constructive feedback is welcome and you can even ask to contribute if you want to.

Thanks, Jerome Lapeyre-Mirande

![alt text](https://github.com/JeromeLM/p-change/blob/master/captures/capture_checker_visible_pwd.PNG?raw=true)
![alt_text](https://github.com/JeromeLM/p-change/blob/master/captures/capture_generator_all_rules.PNG?raw=true)

Installation instructions :
- clone this repository
- create a virtual environment : python -m venv env
- activate this virtual environment : source env/Scripts/activate
- install all the required modules : pip install -r requirements.txt

Use instructions :
- execute the following command : python main.py

