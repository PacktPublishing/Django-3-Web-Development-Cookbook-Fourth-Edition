#!/usr/bin/env bash
echo "=== Deploying project to production server ==="
date

cd "$(dirname "$0")"
ansible-playbook deploy.yml -i hosts/remote --vault-password-file=~/.vault_pass.txt
