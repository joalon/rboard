# RBoard
A reddit clone built with Python, Flask and SQLite.


## Setup
To run a development version with an SQLite database:

```
flask db init
flask db migrate
flask db upgrade

FLASK_ENV=dev flask run
```
