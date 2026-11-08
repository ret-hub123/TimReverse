FROM python:3.11

WORKDIR /app
COPY . /app

RUN apt-get install gcc
RUN pip install uwsgi

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uwsgi", "uwsgi.ini"]