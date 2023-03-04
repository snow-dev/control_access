FROM python:3.3-alpine

ADD main.py .

RUN pip install serial