FROM alpine:3.22

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 \
    py3-pip build-base libffi-dev postgresql-dev \
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

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]