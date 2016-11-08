#!/bin/sh

if [ -n "$USER_PASSWORD" ]; then
	echo "user:$USER_PASSWORD" | chpasswd
fi

if [ $# -lt 1 ]; then
	exec jupyterhub "$@"
else
	exec "$@"
fi
