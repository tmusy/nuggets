FROM postgres:9.5

MAINTAINER Thierry Musy "thierry.musy@gmail.com"

RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

ENV DB_USER nuggets
ENV DB_PASS nuggets

ADD setup-db.sh /docker-entrypoint-initdb.d/
ADD fix-acl.sh /docker-entrypoint-initdb.d/
ADD postgresql.conf /etc/postgres/postgresql.conf

VOLUME /var/lib/postgresql