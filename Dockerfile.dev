FROM python:3.9
WORKDIR "/app"
COPY requirements.txt /
ENV password "$PASSWORD"
ENV host "$HOST"
ENV database "$DATABASE"
ENV user "$USER"
RUN pip install -r /requirements.txt
COPY ./app /app
CMD ["python","./dashboard.py"]