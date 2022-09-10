FROM python:3.10.5

ENV PYTHONUNBUFFERED=1

ADD main.py .
ADD config.py .

RUN pip install requests discord

CMD [ "python", "./main.py" ]