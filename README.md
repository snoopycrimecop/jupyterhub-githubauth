# jupyterhub-githubauth

Dockerfile for the IDR Virtual Analysis Environment.

This uses Jupyterhub, Kubernetes, and optionally Github Authentication.


## Configuration

This image is expected to be run in Kubernetes.
Most variables can be configured using environment variables.
For details see the documentation included in [`jupyterhub_config.py`](jupyterhub_config.py).
