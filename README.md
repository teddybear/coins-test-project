# Test project
## Overview
Web service for transferring coins between accounts

## Requirements
* Python 3.6

## Install
1. Create virtual environment
```
python -m venv .venv
```
2. Activate created environment
```
source .venv/bin/activate
```
3. Install pip requirements
```
pip install -r requirements.txt
```
4. Create and modify environment-related settings (database, secret_key, etc)
```
cp local_settings.example.py local_settings.py
vim local_settings.py
```
5. Run database migrations
```
python manage.py migrate
```
6. Collect static
```
python manage.py collectstatic
```
7. Run tests
```
python manage.py test
```
8. Run linter (in project directory)
```
flake8
```
You'll need to create users and their accounts before using API
```
python manage.py createsuperuser
python manage.py runserver
```
Proceed to http://127.0.0.1:8000/admin with superuser's credentials to add them

## API DOCS
Run local server
```
python manage.py runserver
```
Swagger Docs available from browser http://127.0.0.1:8000/docs

