FROM python:3.9-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]