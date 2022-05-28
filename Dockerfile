FROM bitnami/python:3.9

COPY . /dcp-pde

ENV APP_ROOT=/dcp-pde

WORKDIR /dcp-pde

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip && apt-get update -y
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]