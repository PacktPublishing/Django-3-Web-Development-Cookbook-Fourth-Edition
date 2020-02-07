#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/home/myproject
REPOSITORY_PATH=${PROJECT_PATH}/src/myproject
LOG_FILE=${PROJECT_PATH}/logs/backup_postgres_db.log
DAY_OF_THE_WEEK=$(LC_ALL=en_US.UTF-8 date +"%w-%A")
DAILY_BACKUP_PATH=${PROJECT_PATH}/db_backups/${DAY_OF_THE_WEEK}.backup
LATEST_BACKUP_PATH=${PROJECT_PATH}/db_backups/latest.backup
error_counter=0

echoerr() { echo "$@" 1>&2; }

cd ${PROJECT_PATH}
mkdir -p logs
mkdir -p db_backups

source env/bin/activate
cd ${REPOSITORY_PATH}

DATABASE=$(echo "from django.conf import settings; print(settings.DATABASES['default']['NAME'])" | python manage.py shell -i python)


echo "=== Creating DB Backup ===" > ${LOG_FILE}
date >> ${LOG_FILE}

echo "- Dump database" >> ${LOG_FILE}
pg_dump --format=p --file="${DAILY_BACKUP_PATH}" ${DATABASE}
function_exit_code=$?
if [[ $function_exit_code -ne 0 ]]; then
    {
        echoerr "Command pg_dump failed with exit code ($function_exit_code)."
        error_counter=$((error_counter + 1))
    } >> "${LOG_FILE}" 2>&1
fi

echo "- Create a *.gz archive" >> ${LOG_FILE}
gzip --force "${DAILY_BACKUP_PATH}"
function_exit_code=$?
if [[ $function_exit_code -ne 0 ]]; then
    {
        echoerr "Command gzip failed with exit code ($function_exit_code)."
        error_counter=$((error_counter + 1))
    } >> "${LOG_FILE}" 2>&1
fi

echo "- Create a symlink latest.backup.gz" >> ${LOG_FILE}
if [ -e "${LATEST_BACKUP_PATH}.gz" ]; then
    rm "${LATEST_BACKUP_PATH}.gz"
fi
ln -s "${DAILY_BACKUP_PATH}.gz" "${LATEST_BACKUP_PATH}.gz"
function_exit_code=$?
if [[ $function_exit_code -ne 0 ]]; then
    {
        echoerr "Command ln failed with exit code ($function_exit_code)."
        error_counter=$((error_counter + 1))
    } >> "${LOG_FILE}" 2>&1
fi

duration=$SECONDS
echo "------------------------------------------" >> ${LOG_FILE}
echo "The operation took $((duration / 60)) minutes and $((duration % 60)) seconds." >> ${LOG_FILE}
exit $error_counter