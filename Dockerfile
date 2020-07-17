FROM python:3.7-slim-buster

LABEL maintainer "Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

RUN pip install hpOneView

ADD . oneview/

WORKDIR /root/oneview

CMD ["/bin/bash"]
