
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app


RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app/

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "portal.wsgi:application", "--bind", "0.0.0.0:8000"]
