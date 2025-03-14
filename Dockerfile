FROM python:3

RUN mkdir -p /feeds
RUN mkdir -p /outputs
RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "digestif.py" ]
