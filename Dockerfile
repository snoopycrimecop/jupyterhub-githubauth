FROM jupyterhub/jupyterhub:0.7.2
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

RUN pip install -U pip
RUN pip install dockerspawner==0.7.0
RUN pip install https://github.com/manics/oauthenticator/archive/pr58.zip

RUN useradd user
ADD run.sh /run.sh

ENTRYPOINT ["/run.sh"]
