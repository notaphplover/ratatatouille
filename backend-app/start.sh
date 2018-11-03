#!/usr/bin/env bash

cd /backend-app

python wait-for-mysql.py

cd /backend-app/ratatatouille

if [ "test" = "${APP_ENV}" ]
then
    python manage.py flush --noinput
fi

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

if [ "dev" = "${APP_ENV}" ];
then
    gunicorn ratatatouille.wsgi --bind ":${BACKEND_PORT_INNER}" --reload
elif [ "prod" = "${APP_ENV}" ]
then
    gunicorn ratatatouille.wsgi --bind ":${BACKEND_PORT_INNER}"
elif [ "test" = "${APP_ENV}" ]
then
    python manage.py loaddata ratatatouille-api-restaurants.json
    python manage.py loaddata ratatatouille-api-users.json
    python manage.py loaddata ratatatouille-api-user-permissions.json
    python manage.py test --keepdb
    gunicorn ratatatouille.wsgi --bind ":${BACKEND_PORT_INNER}" --reload
else
    echo "Unexpected application environment ${APP_ENV}"
fi
