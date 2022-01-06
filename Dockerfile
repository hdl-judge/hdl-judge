FROM python:3.10.1-slim-bullseye
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV EXEC_TYPE server
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
CMD [ "sh", "-c", "python ./src/backend/start.py ${EXEC_TYPE}" ]
EXPOSE 8000
