# MAKE SURE YOU DO NOT PUSH THE venv code


To access the website
1. `virtualenv -p python3 venv`
2. `cd venv`
3. `source bin/activate`
4. `cd ..`
5. `pip install django==3.1.2 mysqlclient==2.0.1 pymysql`
6. `python manage.py runserver`
