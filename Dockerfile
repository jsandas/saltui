FROM python:3-alpine

WORKDIR /opt/saltui

ADD ./ /opt/saltui

RUN apk add --no-cache --virtual .build-deps build-base libffi-dev rust cargo openssl-dev postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && apk add --no-cache libpq \
    && wget -O /usr/local/bin/wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for \
    && chmod +x /usr/local/bin/wait-for

RUN adduser -u 978 -h /opt/saltui -g 'python app user' -s /sbin/nologin -D python
    # && chown -R python:python /opt/saltui

EXPOSE 8080

# USER python

CMD ["/opt/saltui/start.sh"]
