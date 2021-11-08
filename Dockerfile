FROM python:3.8-slim-buster
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV EXEC_TYPE server
CMD [ "sh", "-c", "python ./src/back/start.py ${EXEC_TYPE}" ]
EXPOSE 8080
