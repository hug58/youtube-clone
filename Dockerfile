FROM python:3.12.6


WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .
EXPOSE 8000


CMD ["gunicorn", "backend.wsgi:application", "--config", "gunicorn.py"]
