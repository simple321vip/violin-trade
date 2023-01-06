FROM ccr.ccs.tencentyun.com/violin/violin-trade-base:latest

ADD app /apps/app
ADD strategy /apps/strategy
ADD vnpy /apps/vnpy

COPY manage.py /apps/
COPY config.py /apps/

RUN dpkg-reconfigure locales
RUN cat /etc/default/locale

EXPOSE 8080

WORKDIR /apps

ENTRYPOINT ["python", "manage.py"]