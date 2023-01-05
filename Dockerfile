FROM ccr.ccs.tencentyun.com/violin/violin-trade-base:latest

COPY app /apps

COPY manage.py /apps

COPY strategy /apps

EXPOSE 8080

WORKDIR /apps

ENTRYPOINT ["python", "manage.py"]
