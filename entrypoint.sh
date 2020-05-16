#!/bin/sh

if [ -z $FLASK_ENV ]; then
    echo "No FLASK_ENV variable set"
    exit 1
elif [[ "$FLASK_ENV" == "dev" ]]; then
    flask db init
    flask db migrate
    flask db upgrade
elif [[ "$FLASK_ENV" == "prod" ]]; then
    flask db upgrade
else
    echo "Expected FLASK_ENV to be one of \"prod\" or \"dev\""
    exit 1
fi

flask run --host=0.0.0.0
