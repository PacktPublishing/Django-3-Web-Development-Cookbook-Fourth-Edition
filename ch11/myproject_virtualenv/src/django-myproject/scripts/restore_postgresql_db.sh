#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/home/myproject
REPOSITORY_PATH=${PROJECT_PATH}/src/myproject
LATEST_BACKUP_PATH=${PROJECT_PATH}/db_backups/latest.backup
export DJANGO_SETTINGS_MODULE=myproject.settings.production

cd "${PROJECT_PATH}"
source venv/bin/activate

cd "${REPOSITORY_PATH}"

DATABASE=$(echo "from django.conf import settings; print(settings.DATABASES['default']['NAME'])" | python manage.py shell -i python)
USER=$(echo "from django.conf import settings; print(settings.DATABASES['default']['USER'])" | python manage.py shell -i python)
PASSWORD=$(echo "from django.conf import settings; print(settings.DATABASES['default']['PASSWORD'])" | python manage.py shell -i python)

echo "=== Restoring DB from a Backup ==="

echo "- Recreate the database"
psql --dbname=$DATABASE --command='SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();'
dropdb $DATABASE
createdb --username=$USER $DATABASE

echo "- Fill the database with schema and data"
zcat "${LATEST_BACKUP_PATH}.gz" | python manage.py dbshell

duration=$SECONDS
echo "------------------------------------------"
echo "The operation took $((duration / 60)) minutes and $((duration % 60)) seconds."
