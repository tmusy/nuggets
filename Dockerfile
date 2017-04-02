FROM python:3.6-slim
MAINTAINER Thierry Musy <thierry.musy@gmail.com>

ENV INSTALL_PATH /nuggets
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
#RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "nuggets.app:create_app()"