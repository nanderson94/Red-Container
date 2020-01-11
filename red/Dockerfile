FROM python:3.8.1-alpine

WORKDIR /app
VOLUME [ "/app/data" ]
EXPOSE 6133

RUN pip install --no-cache-dir Red-DiscordBot[postgres]
COPY . .
CMD [ "python" "./red-launcher.py" ]
