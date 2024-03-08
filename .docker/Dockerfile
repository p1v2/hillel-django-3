#FROM python:3.12-slim
#
#WORKDIR /app
#
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    python3-dev \
#    postgresql-client \
#    redis-tools
#RUN apt-get install -y libpq-dev
#
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#RUN apt-get update && apt-get install -y gunicorn redis-server
#
#COPY . .
#
#RUN gunicorn --bind 0.0.0.0:8000 hillelDjango3.wsgi:application
##    celery -A hillelDjango3 worker --loglevel=info & \
##    redis-server
#
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hillelDjango3.wsgi:application"]
