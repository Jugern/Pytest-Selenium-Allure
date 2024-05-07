FROM python:3.11-alpine3.19

RUN echo "https://dl-4.alpinelinux.org/alpine/v3.19/main" >> /etc/apk/repositories && \
    echo "https://dl-4.alpinelinux.org/alpine/v3.19/community" >> /etc/apk/repositories

RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk

RUN apk update && \
    apk add --no-cache bash && \
    apk add openjdk11-jre curl tar && \
    curl -o allure-2.13.8.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz && \
    tar -zxvf allure-2.13.8.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm allure-2.13.8.tgz

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ./wait-for-it.sh selenium-hub:${port_selenium_grid} -- pytest -sv && allure generate --clean && allure open --port 9999

