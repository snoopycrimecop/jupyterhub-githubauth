#!/bin/bash

set -eux

docker build -t test-jupyterhub-githubauth .
docker run -d -e JUPYTERHUB_PROXY_SERVICE_HOST=localhost -e JUPYTERHUB_PROXY_SERVICE_PORT=0 -p 8000:8000 --name test-jupyterhub-githubauth test-jupyterhub-githubauth
sleep 10
R=$(curl -f http://localhost:8000/hub/api)
test "$R" = '{"version": "0.7.2"}'
docker rm -f test-jupyterhub-githubauth
