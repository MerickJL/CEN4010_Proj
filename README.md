# FIU CEN4010 group project - Bookstore API

This API will be used as part of the backend for a bookstore website.

# Setup environment

Make sure you have a Python version installed and added to your PATH

### Install dependencies/requirements. There are in order of how I did them to work. 

 1. If you want to have a specific environment run:

            pip3 install pipenv # Only the first time
            pipenv lock --pre --clear
            pipenv shell

  2.  Intalling Flask

             pipenv install flask

  3.  Installing Marshmallow API

                pipenv install marshmallow

  4.  Installing SQLAlchemy

                pipenv install sqlalchemy

If you want to install all the packages system-wide:

    pip3 install -r requirements.txt

Install SQLlite (back up just in case SQLAlchemy doesn't work)

    pipenv install pysqlite3

# Launch server

    python3 BookstoreAPI.py

or

    python BookstoreAPI.py

# Sending POST and GET requests

Postman is now an extension in VS Code.
Code will be done on a local host, ie http://localhost:_assignedPortfromBookstoreAPI_/_AppRoute_/
