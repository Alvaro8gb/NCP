
#FROM ubuntu:18.04
FROM python:3.10

WORKDIR /ncp
ADD . /ncp

RUN pip install -r /ncp/requirements.txt 

EXPOSE 8000
ENTRYPOINT ["python", "/ncp/api.py"]
