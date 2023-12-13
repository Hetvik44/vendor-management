## Setup

* Clone project
  `git clone https://github.com/Hetvik44/vendor-management.git`
  `$ cd vendor-management`
* Create virtualenv using python3

    `$ python3 -m virtualenv venv`

* Activate virtualenv for linux users

    `$ source venv/bin/activate`

* Now install all requirements

    `$ pip install -r requirements.txt`

 
* Create .env file using given environment file template.

    `$ cp .env.template .env`

* Now migrate models in db

    `$ python manage.py migrate`
    
* Create superuser to login to django admin.

    `$ python manage.py createsuperuser`
    
* All done now run following command for running your server

    `$ python manage.py runserver "port_number"`


* Create a Normal User through Django Admin
Access Django Admin at http://127.0.0.1:{port_number}/admin/
Log in with the superuser credentials created in step 7.
Create a normal user through the Django admin interface.


* Obtain Authentication Token
Use the login API to obtain an authentication token using user username and password.


* Create Vendor and Use Other APIs
Use the obtained authentication token to access other APIs.


* API Documentation
View API documentation at http://127.0.0.1:{port_number}/
