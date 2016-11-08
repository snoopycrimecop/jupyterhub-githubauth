FROM jupyterhub/jupyterhub:0.6.1
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

RUN pip install -U pip
RUN pip install dockerspawner==0.4.0 oauthenticator

RUN useradd user
ADD run.sh /run.sh

ENTRYPOINT ["/run.sh"]
