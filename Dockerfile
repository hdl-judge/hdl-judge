FROM node AS builder
WORKDIR /tmp
COPY src/frontend/package.json /tmp
RUN npm i
COPY src/frontend /tmp
RUN npm run build

FROM python:3.10.1
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
COPY --from=builder /tmp/public/* /app/static/*
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD [ "python", "./src/backend/start.py", "server", "80" ]
