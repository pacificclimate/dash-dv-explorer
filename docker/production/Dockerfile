FROM python:3.6-slim
MAINTAINER Rod Glover <rglover@uvic.ca>

RUN apt-get update && \
    apt-get install -y git && \
    pip install --upgrade pip

ARG RUN_GROUP=dve
ARG RUN_USER=dve
ARG RUN_HOME=/app

RUN groupadd -r ${RUN_GROUP} && \
    useradd -g ${RUN_GROUP} -d ${RUN_HOME} ${RUN_USER} && \
    mkdir ${RUN_HOME} && \
    chown ${RUN_GROUP}:${RUN_USER} ${RUN_HOME}
USER ${RUN_USER}

WORKDIR ${RUN_HOME}
COPY --chown=${RUN_GROUP}:${RUN_USER} . /app

RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt && \
    pip install -e git+https://github.com/pacificclimate/climpyrical.git#egg=climpyrical && \
    pip install /app

# Flask app port
EXPOSE 5000

ENV NAME Explorer

CMD /app/.local/bin/gunicorn \
    --config /app/docker/production/gunicorn.conf \
    --log-config /app/docker/production/logging.conf \
    dve_app:server
