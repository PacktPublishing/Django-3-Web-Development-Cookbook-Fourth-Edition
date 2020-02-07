#!/usr/bin/env bash
echo "=== Setting up the production server ==="
date

cd "$(dirname "$0")"
ansible-playbook setup.yml -i hosts/remote