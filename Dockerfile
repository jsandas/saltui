FROM python:3-alpine

WORKDIR /opt/saltui

COPY ./ /opt/saltui

# build dependencies
RUN apk add --no-cache --virtual .build-deps build-base libffi-dev postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# install required packages/scripts
RUN apk add --no-cache libpq openssl
RUN wget -O /usr/local/bin/wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for \
    && chmod +x /usr/local/bin/wait-for

RUN openssl req -x509 -nodes -days 365 \
    -subj "/C=CA/ST=QC/O=Company, Inc./CN=mydomain.com" \
    -addext "subjectAltName=DNS:mydomain.com" \
    -newkey rsa:2048 -keyout /etc/ssl/private/selfsigned.key \
    -out /etc/ssl/certs/selfsigned.crt

RUN adduser -u 978 -h /opt/saltui -g 'python app user' -s /sbin/nologin -D python
    # && chown -R python:python /opt/saltui

EXPOSE 8080

# USER python

CMD ["/opt/saltui/start.sh"]
