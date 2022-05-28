FROM bitnami/python:3.9

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --upgrade pip && apt-get update -y
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]