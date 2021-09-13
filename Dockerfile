FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip portaudio19-dev python-pyaudio
COPY /Worker /opt/Worker/
RUN pip3 install -r /opt/Worker/requirements.txt
ENV PYTHONPATH /opt/Worker/
WORKDIR /opt/Worker/
CMD ["python3","StreamingServer.py"]
