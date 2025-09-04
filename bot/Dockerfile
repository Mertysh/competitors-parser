FROM python:3.10-slim-bullseye

WORKDIR /repricer
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH=/root/.local/bin:$PATH

COPY . .
CMD python bot.py
