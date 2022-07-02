FROM docker.io/mambaorg/micromamba:latest

WORKDIR /home/mambauser

# RUN source /usr/local/bin/_activate_current_env.sh && \
RUN micromamba install -p /opt/conda/ -c defaults -y -q \
        git \
        pip && \
    /opt/conda/bin/pip install \
        'jupyterlite[contents]' \
        jupyterlite-xeus-python

COPY jupyter_lite_config.json /home/mambauser/

# Running this now will speed up the next build with dependencies
RUN /opt/conda/bin/jupyter lite build

COPY build.py /home/mambauser/
