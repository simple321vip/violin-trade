FROM ccr.ccs.tencentyun.com/violin/violin-trade-base:latest

ADD app /apps/app
ADD strategy /apps/strategy
ADD vnpy /apps/vnpy

COPY manage.py /apps/
COPY config.py /apps/

RUN echo 'LANG="zh_CN.UTF-8"' > /etc/default/locale
RUN echo 'LANGUAGE="zh_CN:zh"' >> /etc/default/locale
RUN sudo apt-get clean && apt-get update && apt-get install -y locales
RUN sudo locale-gen zh_CN.GB18030

EXPOSE 8080

WORKDIR /apps

ENTRYPOINT ["python", "manage.py"]