FROM python:3.6.2-alpine3.6

ADD files/ /files
RUN pip install -r /files/requirements.txt

ADD api /api
ADD example.py /example.py

ENTRYPOINT ["python", "/example.py"]