FROM python:3.10.7

ENV PYTHONUNBUFFERED=1

ADD main.py .
ADD config.py .

RUN pip install requests discord millify

CMD [ "python", "./main.py" ]