# base image ccr.ccs.tencentyun.com/violin/violin-trade-base
# first stage
FROM python:3.10.8 as builder

RUN python -m pip install --upgrade pip

# to install package and delete tmp files.
# RUN pip install vnpy && find /usr/local/lib -name '*.pyc' -delete
COPY requirements.txt .

RUN pip install -r requirements.txt --timeout=1600 -i https://pypi.tuna.tsinghua.edu.cn/simple

# second stage
FROM python:3.10.8-slim

# copy compiled lib from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

RUN rm -rf /etc/apt/sources.list

COPY sources.list /etc/apt/

RUN apt-get clean -y && apt-get update -y && apt-get upgrade -y
RUN apt-get install locales -y

RUN mkdir /apps

WORKDIR /apps

# to set locales and commit to image
ENTRYPOINT cat
