FROM centos:8

RUN yum install -y python3 python3-pip

RUN useradd -d /opt/rboard --shell /bin/bash rboard
USER rboard
WORKDIR /opt/rboard

COPY --chown=rboard rboard ./rboard
COPY --chown=rboard requirements.txt app.py entrypoint.sh /opt/rboard/

RUN pip3 install --user -r requirements.txt

ENV FLASK_APP rboard
ENV FLASK_ENV dev
ENV PATH "/opt/rboard/.local/bin:${PATH}"

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
