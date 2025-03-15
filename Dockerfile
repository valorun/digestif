FROM python:3

ENV FEEDS_PATH=/feeds
ENV OUTPUT_PATH=/outputs

RUN mkdir -p /feeds
RUN mkdir -p /outputs
RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "digestif.py" ]
