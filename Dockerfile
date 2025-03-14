FROM ghcr.io/prefix-dev/pixi:0.39.3-bullseye
RUN apt-get update && apt-get upgrade -y && apt-get install -y git
RUN mkdir -p /feeds
RUN mkdir -p /outputs
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .
CMD ["/usr/local/bin/pixi", "run", "start"]
