FROM python:3.7

WORKDIR /app

RUN apt update
RUN apt install libsecp256k1-dev --assume-yes
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip==20.2.4
COPY scanner_requirements.txt /app/
RUN pip install -r scanner_requirements.txt

EXPOSE 8000

COPY . /app

CMD ["python", "scanner/networks/networks_scan_entrypoint.py"]
