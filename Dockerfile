FROM python:3.8
COPY requirements.txt .
RUN pip3 install -r --user requirements.txt
RUN playwright install

ADD . /app
WORKDIR /app/

CMD ["airflow", "standalone"]
