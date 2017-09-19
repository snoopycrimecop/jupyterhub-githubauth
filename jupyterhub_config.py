import json
import os


######################################################################
# Jupyterhub settings
######################################################################

# The class used to spawn new singleuser servers
c.JupyterHub.spawner_class = os.getenv('IDR_JUPYTER_SPAWNER_CLASS', 'kubespawner.KubeSpawner')
c.JupyterHub.ip = '0.0.0.0'

# Jupyterhub proxy token, optional but recommened otherwise
# singleuser servers may become unreachable aftger a restart
c.JupyterHub.proxy_auth_token = os.getenv('IDR_JUPYTER_PROXY_TOKEN', '')

# Whitespace separated list of users
c.Authenticator.whitelist = os.getenv('IDR_JUPYTER_USERS', '').split()
# Whitespace separated list of admins
c.Authenticator.admin_users = os.getenv('IDR_JUPYTER_ADMINS', '').split()

# The authenticator class
# You can set this to dummyauthenticator.DummyAuthenticator for testing
c.JupyterHub.authenticator_class = os.getenv('IDR_JUPYTER_AUTHENTICATOR', 'jupyterhub.auth.PAMAuthenticator')

c.JupyterHub.services = [
  {
    'name': 'cull-idle',
    'admin': True,
    'command': [
      'python',
      '/srv/jupyterhub/cull_idle_servers.py',
      '--timeout=3600',
    ],
  }
]


######################################################################
# KubeSpawner settings
# Ignored for other spawners
######################################################################

# Kubernetes namespace
c.KubeSpawner.namespace = os.getenv('POD_NAMESPACE', 'default')
# Timeout for pulling images in seconds, increase this for large images
c.KubeSpawner.start_timeout = os.getenv('IDR_JUPYTER_START_TIMEOUT', 300)

# Single user notebook image
c.KubeSpawner.singleuser_image_spec = os.getenv('IDR_JUPYTER_IMAGE', 'imagedata/jupyter-docker:develop')
c.KubeSpawner.singleuser_uid = 1000
c.KubeSpawner.singleuser_fs_gid = 100

c.KubeSpawner.hub_connect_ip = os.environ['JUPYTERHUB_PROXY_SERVICE_HOST']
c.KubeSpawner.hub_connect_port = int(os.environ['JUPYTERHUB_PROXY_SERVICE_PORT'])

# Setup two volumes, one for the user and open shared amongst all users
c.KubeSpawner.volumes = [
  {
    'name': 'jupyter-scratch-{username}',
    'persistentVolumeClaim': {'claimName': 'jupyter-scratch-{username}'}
  },
  {
    'name': 'jupyter-sharedscratch',
    'persistentVolumeClaim': {'claimName': 'jupyter-sharedscratch-rw'}
  },
]
c.KubeSpawner.volume_mounts = [
  {
    'mountPath': '/notebooks/scratch',
    'name': 'jupyter-scratch-{username}'
  },
  {
    'mountPath': '/notebooks/shared',
    'name': 'jupyter-sharedscratch'
  },
]

c.KubeSpawner.pvc_name_template = 'jupyter-scratch-{username}'
# This isn't actually enforced on NFS
c.KubeSpawner.user_storage_capacity = '100M'
# The storage provisioner, you must change this to a provisioner that
# already exists in your Kubernetes cluster
c.KubeSpawner.user_storage_class = os.getenv('IDR_JUPYTERHUB_STORAGE_CLASS', 'dynamic-nfs-volume')
c.KubeSpawner.user_storage_access_modes = ['ReadWriteMany']
c.KubeSpawner.user_storage_pvc_ensure = True


######################################################################
# Github authentication settings
# Ignored for other authenticators
#
# The IDR VAE uses a modification of the upstream Github
# authenticator: https://github.com/IDR/oauthenticator
# To enable this use oauthenticator.GitHubOrgOAuthenticator
#
# See:
# - https://github.com/settings/developers
# - https://github.com/IDR/oauthenticator/
######################################################################

c.GitHubOAuthenticator.oauth_callback_url = os.getenv('IDR_JUPYTER_OAUTH_CALLBACK', '')
c.GitHubOAuthenticator.client_id = os.getenv('IDR_JUPYTER_GITHUB_ID', '')
c.GitHubOAuthenticator.client_secret = os.getenv('IDR_JUPYTER_GITHUB_SECRET', '')
# Currently relying on https://github.com/IDR/oauthenticator/pull/3
# which only supports a single Github organisation
# Functionality for multiple organisations was added in an upstream PR
# but it doesn't work:
# https://github.com/jupyterhub/oauthenticator/pull/58#issuecomment-290442794
#c.GitHubOAuthenticator.github_organization_whitelist = {{ idr_jupyter_github_orgs | to_json }}
c.GitHubOrgOAuthenticator.github_organization_whitelist = os.getenv('IDR_JUPYTER_GITHUB_ORGS', '').split()
# Multiple hostnames/tokens for github oauth (optional):
# https://github.com/IDR/oauthenticator/pull/3
c.GitHubOAuthenticator.oauth_callback_url_hostmap = json.loads(os.getenv('IDR_JUPYTER_GITHUB_CALLBACK_HOSTMAP', '{}'))
c.GitHubOAuthenticator.client_id_hostmap = json.loads(os.getenv('IDR_JUPYTER_GITHUB_CLIENT_ID_HOSTMAP', '{}'))
c.GitHubOAuthenticator.client_secret_hostmap = json.loads(os.getenv('IDR_JUPYTER_GITHUB_SECRET_HOSTMAP', '{}'))
