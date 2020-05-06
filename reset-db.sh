#!/bin/sh

rm -rf migrations
rm app/test.db

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
