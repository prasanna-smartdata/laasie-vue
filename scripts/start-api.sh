#!/bin/bash

export FLASK_APP=api

if [[ "$EUID" -ne 0 ]]; then
    echo "******"
    echo "Please run this script with sudo due to binding to a privileged port"
    echo "******"
    exit 1
fi

# --debug will set FLASK_DEBUG to True automatically.
flask --debug --app api:create_app run --cert ./api/localhost.crt --key ./api/localhost.key -p 443
