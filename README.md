# FIU CEN4010 group project - Bookstore API

This API will be used as part of the backend for a bookstore website.

# Setup environment

Make sure you have a [python3](https://www.python.org/ftp/python/3.6.6/python-3.6.6-amd64.exe) version installed and added to your PATH

### Get the repo on your computer

If you are on Windows, you can use [Git Bash](https://git-scm.com/download/win).
If you are using vscode/pycharm, look up a video on how to use git with those.

### Clone the repository

    git clone 'https://github.com/CEN4010-Group-5/BookstoreAPI.git'

### Go to the project's directory

    cd BookstoreAPI

### Create your feature's branch

    git checkout -b FeatureName # Create
    git checkout FeatureName # Swap to your branch

### Install dependencies/requirements

If you want to have a specific environment run:

    pip3 install pipenv # Only the first time
    pipenv lock --pre --clear
    pipenv shell

If you want to install all the packages system-wide:

    pip3 install -r requirements.txt

# How to clear/refactor the database

This will be need to be done if there are any changes in the class schema

    remove the db.sqlite file
    Launch the server normally and the tables will be created

# Launch server

    python3 BookstoreAPI.py

or

    python BookstoreAPI.py

# Sending POST and GET requests

You can use [Postman](https://www.postman.com/) for a more visual approach.
You can refer to this [YouTube video](https://www.youtube.com/watch?v=PTZiDnuC86g) for a guide
