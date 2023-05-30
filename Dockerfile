FROM python:3.9


COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN apt-get update && apt-get install -y curl

COPY docker-entrypoint-initdb.d /docker-entrypoint-initdb.d

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]