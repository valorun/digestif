FROM ghcr.io/prefix-dev/pixi:0.39.3-bullseye
RUN apt-get update && apt-get upgrade -y && apt-get install -y git
WORKDIR /app
COPY . .
EXPOSE 8080
CMD ["/usr/local/bin/pixi", "run", "start"]
