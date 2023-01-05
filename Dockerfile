FROM ccr.ccs.tencentyun.com/violin/violin-trade-base:latest

ADD app /apps/app
ADD strategy /apps/strategy

COPY manage.py /apps/
COPY config.py /apps/

EXPOSE 8080

WORKDIR /apps

ENTRYPOINT ["python", "manage.py"]