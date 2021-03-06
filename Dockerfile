# Alpine for smaller size
FROM python:3.9-alpine

# Create a system account hubibot.hubibot
RUN addgroup -S awair && adduser -S awair -G awair
# Non-alpine equivalent of above:
#RUN groupadd -r awair && useradd -r -m -g awair awair

# One of the Python packages has a dependency on gcc to install
# https://github.com/closeio/ciso8601/issues/98
RUN apk add build-base 

USER awair

WORKDIR /app

# set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt     /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt --no-warn-script-location 

COPY *.py              /app/
COPY template.config.yaml /app/

ENTRYPOINT python main.py
