FROM python:3
ENV PYTHONPATH $PYTHONPATH:.
ADD ingest_document.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["twistd", "-n", "web", "--port", "8080", "--wsgi", "ingest_document.app"]
