# Django Docker

## 1. Create executable build_dev.sh

Copy `build_dev_example.sh` to `build_dev.sh`.

Edit the `build_dev.sh` file and add sensible values there.

Add execution permissions:

```bash
$ chmod +x build_dev.sh
```

## 2. Build the Docker containers

Run `build_dev.sh`:

```bash
$ ./build_dev.sh
```

## 3. Check if the build was successful

If you now go to `http://0.0.0.0/` you should see a "Hello, World!" page there.

If you now go to `http://0.0.0.0/admin/`, you should see 

```
OperationalError at /admin/
FATAL:  role "myproject" does not exist
```

This means that you have to create the database user and the database in the Docker container.

## 4. Create database user and project database

SSH into the database container and create user and database there with the same values as in the `.build_dev.sh` script:

```bash
$ docker exec -it myproject_docker_db_1 bash
/# su - postgres
/$ createuser --createdb --password myproject
/$ createdb --username myproject myproject
```

When asked, enter the same password for the database as in the `build_dev.sh` script.

Press [Ctrl + D] twice to logout of the postgres user and Docker container.

If you now go to `http://0.0.0.0/admin/`, you should see 

```
ProgrammingError at /admin/
relation "django_session" does not exist
LINE 1: ...ession_data", "django_session"."expire_date" FROM "django_se...
```

This means that you have to run migrations to create database schema.

## 5. Run migration and collectstatic commands

SSH into the gunicorn container and run the necessary Django management commands:

```bash
$ docker exec -it myproject_docker_gunicorn_1 bash
$ source env/bin/activate
(env)$ python manage.py migrate
(env)$ python manage.py collectstatic
(env)$ python manage.py createsuperuser
```

Answer all the questions asked by the management commands.

Press [Ctrl + D] twice to logout of the Docker container.

If you now go to `http://0.0.0.0/admin/`, you should see the Django administration where you can login with the super user's credentials that you have just created.

## 6. Overview of useful commands

### Rebuild docker containers

```bash
$ docker-compose down
$ ./build_dev.sh
```

### SSH to the Docker containers

```bash
$ docker exec -it myproject_docker_gunicorn_1 bash
$ docker exec -it myproject_docker_nginx_1 bash
$ docker exec -it myproject_docker_db_1 bash
```

### View logs

```bash
$ docker-compose logs nginx
$ docker-compose logs gunicorn
$ docker-compose logs db
```

### Copy files and directories to and from Docker container

```bash
$ docker cp ~/avatar.png myproject_docker_gunicorn_1:/home/myproject/media/
$ docker cp myproject_docker_gunicorn_1:/home/myproject/media ~/Desktop/
```

## 7. Create analogous scripts for staging, production, and test environments

Copy `build_dev.sh` to `build_staging.sh`, `build_production.sh`, and `build_test.sh` and change the environment variables analogously.

## 8. Feedback

If you have any feedback about the boilerplate code or this README file, please open new issues.
