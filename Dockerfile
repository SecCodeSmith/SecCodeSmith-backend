FROM alpine:3.22

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add --update --no-cache --virtual .build-deps \
        build-base \
        libffi-dev \
        postgresql-dev \
    && apk add --update --no-cache \
        python3 \
        py3-pip \
        bash \
        postgresql-client \
        tzdata \
    && ln -sf python3 /usr/bin/python

RUN python3 -m venv /opt/venv

RUN mkdir /app
WORKDIR /app

COPY requirements.txt  .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8000

CMD ["gunicorn", "SecCodeSmithBackend.wsgi:application", "--bind", "0.0.0.0:8000"]