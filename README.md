# Project Setup Guide

## 1. Installing Project Dependencies
After cloning the application, run following command to install all the required dependencies.

```
pip install -r Requirements.txt
```

## 2. Setting up environment variables
Create `.env` file in same directory as `manage.py` file. Set the values of following variables

```
DJANGO_SECRET_KEY=
DEBUG=
DATABASE_HOST=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
```

## 3. Creating Database
Configure database settings in `AltText/settings.py` if required. Create a database in mysql with the name 'alttext'.

## 4. Applying Migrations
Change directory to AltText directory containing the `manage.py` file and run the following command.

```
python3 manage.py makemigrations
```

After the migrations have been create apply them with the help of follwing command.

```
python3 manage.py migrate
```

## 5. Running The Application
Run the server with the given command.

```
python3 manage.py runserver
```
