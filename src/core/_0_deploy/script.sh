#!/bin/sh

set -e

GUNICORN_BIND_PORT=${DJANGO_PORT:-8000}

echo "⏸️ Waiting for Database port to be open..."
while ! nc -z ${DATABASES_HOST:-maria_db} ${DATABASES_PORT:-3306}; do
    sleep 1
done
echo "✅ Database is reachable. Waiting an extra 5 seconds for full readiness..."
sleep 5

echo "✅ Start makemigrations and migrate"
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "✅ Start Collect Static ..."
python manage.py collectstatic --noinput

# for force update static file
# python manage.py collectstatic --noinput --clear --verbosity 0

echo "✅ Checking User ..."
python manage.py shell << EOF
from _2_account.views.base.views_user import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
    print("✅ Superuser created.")
else:
    print("ℹ️ Superuser already exists.")
EOF

gunicorn _0_config.wsgi -b 0.0.0.0:"$GUNICORN_BIND_PORT"