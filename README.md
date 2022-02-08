# installation

`pipenv install`

load database with basic fixtures

`python manage.py migrate && python manage.py loaddata core/fixtures/{users.products}.json`.

then do the following command to run the server:

`python manage.py runserver`
