FROM python:3.9.0

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt

CMD python /code/manage.py runserver 0:8000