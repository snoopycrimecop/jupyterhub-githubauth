#!/bin/sh

if [ -n "$USER_PASSWORD" ]; then
	echo "user:$USER_PASSWORD" | chpasswd
fi
exec jupyterhub "$@"
