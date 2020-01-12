#!/usr/bin/env bash
echo "=== Setting up the local staging server ==="
date

cd "$(dirname "$0")"
vagrant up --provision
