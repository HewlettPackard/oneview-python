FROM python:3.7-slim-buster


LABEL maintainer "Priyanka Sood <priyanka.sood@hpe.com>"

RUN pip install hpOneView==5.0.0

CMD ["/bin/bash"]
