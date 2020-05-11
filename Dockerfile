FROM centos:8

RUN yum install -y python3 python3-pip

RUN useradd -d /opt/rboard --shell /bin/bash rboard
USER rboard
WORKDIR /opt/rboard

COPY rboard ./rboard
COPY requirements.txt .

RUN pip3 install --user -r requirements.txt

ENV FLASK_APP rboard
ENV FLASK_ENV dev

CMD flask run
