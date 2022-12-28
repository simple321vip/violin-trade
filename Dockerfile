FROM ccr.ccs.tencentyun.com/violin/violin-trade-base:latest

RUN mkdir /apps

WORKDIR /apps

COPY nginx.conf /etc/nginx/conf.d/default.conf