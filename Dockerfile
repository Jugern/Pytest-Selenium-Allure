FROM python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt .
COPY . /usr/src/app
RUN chmod +x wait-for-it.sh
RUN pip install -r requirements.txt