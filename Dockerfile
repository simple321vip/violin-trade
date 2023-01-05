FROM ccr.ccs.tencentyun.com/violin/violin-trade-base:latest

ADD app /apps/app

COPY manage.py /apps/

ADD strategy /apps/strategy

EXPOSE 8080

WORKDIR /apps

ENTRYPOINT ["python", "manage.py"]