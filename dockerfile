FROM python:3.8-slim-buster
RUN python3 -m venv /opt/venv

COPY ./src /src
COPY ./test /test

RUN . /opt/venv/bin/activate
CMD . /opt/venv/bin/activate  && ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]