#!/usr/bin/env bash
coverage erase
coverage run manage.py test --settings=myproject.settings.test
coverage report