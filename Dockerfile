FROM python:3.6-slim-buster

ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV http_proxy=$http_proxy
ENV https_proxy=$https_proxy
ENV no_proxy=$no_proxy

WORKDIR /root

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y \
    vim curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* /tmp/*

RUN python -m pip install --upgrade pip


RUN pip install future==0.18.2


RUN pip install hpeOneView


COPY . /root/oneview
WORKDIR /root/oneview

RUN pip install -r test_requirements.txt && \
    pip install tox

CMD ["/bin/bash"]
