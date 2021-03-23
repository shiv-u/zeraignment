web: python manage.py collectstatic --no-input; gunicorn marketinfo.wsgi:application -w 2 -b :$PORT
