FROM jupyterhub/jupyterhub:0.6.1
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

RUN pip install -U pip
RUN pip install dockerspawner==0.7.0
RUN pip install https://github.com/IDR/oauthenticator/archive/0.5.1-IDR1.zip

RUN useradd user
ADD run.sh /run.sh

ENTRYPOINT ["/run.sh"]
