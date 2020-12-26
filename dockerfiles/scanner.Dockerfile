FROM python:3.7
RUN apt update
RUN apt install libsecp256k1-dev --assume-yes
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip==20.2.4
COPY scanner_requirements.txt /code/
RUN pip install -r scanner_requirements.txt

EXPOSE 8000

COPY . /code/

CMD ["python", "scanner/networks/networks_scan_entrypoint.py"]
