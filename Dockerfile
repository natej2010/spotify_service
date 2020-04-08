FROM python

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEYBTECODE 1
ENV PYTHONUNBUFFERED 1
ENV GOOGLE_APPLICATION_CREDENTIALS="CacheMemoryMillionaires-e5728027d964.json"

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/
