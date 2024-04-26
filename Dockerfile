FROM ubuntu:latest

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3.10 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN chmod +x fetch_and_run.sh

ENTRYPOINT ["./fetch_and_run.sh"]
