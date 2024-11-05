FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt --no-cache-dir && rm -rf /var/lib/apt/lists/*

COPY ./bookshop /app

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]