FROM alpine:3.22

ENV PYTHONUNBUFFERED=1
ENV DATABASE_HOST="postgres:5432"
ENV DATABASE_USER="postgres"
ENV DATABASE_PASSWORD="postgres"
ENV DATABASE_NAME="app"

ENV EMAIL_HOST=""
ENV EMAIL_LOGIN=""
ENV EMAIL_PASSWORD=""
ENV EMAIL_SMTP_PORT=""
ENV EMAIL=""

ENV REDIS_HOST=""
ENV REDIS_PORT=""
ENV REDIS_PASSWORD=""

RUN apk add --update --no-cache python3 \
    py3-pip build-base libffi-dev postgresql-dev \
    bash \
    && ln -sf python3 /usr/bin/python

RUN mkdir /app
WORKDIR /app

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

COPY requirements.txt  /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . /app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8000

CMD ["python", "manage.py runserver 0.0.0.0:8000"]