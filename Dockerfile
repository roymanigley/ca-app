FROM python:3.11-alpine

RUN apk update && apk upgrade --no-cache
RUN apk add gettext

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DEBUG false
ENV DJANGO_LOGGING_DIR '/var/log/ca-app/'
ENV DJANGO_DB_DIR '/var/data/ca-app/db'
ENV DJANGO_STATIC_DIR '/var/data/ca-app/static'
ENV DJANGO_MEDIA_DIR '/var/data/ca-app/media'
RUN mkdir -p ${DJANGO_LOGGING_DIR}
RUN mkdir -p ${DJANGO_DB_DIR}
RUN mkdir -p ${DJANGO_STATIC_DIR}
RUN mkdir -p ${DJANGO_MEDIA_DIR}

WORKDIR /opt/app

COPY requirements.txt /opt/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /opt/app/

RUN addgroup -S app-group && adduser -S app-user -G app-group
RUN chown app-user:app-group ${DJANGO_LOGGING_DIR} -R
RUN chown app-user:app-group ${DJANGO_DB_DIR} -R
RUN chown app-user:app-group ${DJANGO_STATIC_DIR} -R
RUN chown app-user:app-group ${DJANGO_MEDIA_DIR} -R

USER app-user

CMD ["./entrypoint.sh"]
