FROM docker.io/library/python:3.12-slim

# Avoid interactive package prompts and unbuffer Python logs.
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt/app/
WORKDIR /opt/app/
COPY ./main.py main.py
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt;
CMD ["python","/opt/app/main.py"]