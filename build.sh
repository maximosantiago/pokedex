#!/usr/bin/env bash
# exit on error

set -o errexit

pip install -r requirements.txt



python manage.py collectstatic --no-input
python manage.py migrate

#con este archivo, le indicamos a render donde va a estar los archivos estaticos, tambien le indicamos que las migraciones las realizara automaticamente. y ademas le indicamos que herramientas va a utilizar