FROM python:3.10

WORKDIR /app

ENV BOT_TOKEN=XXX
ENV PYLOAD_ADDRESS=XXX
ENV PYLOAD_USERNAME=XXX
ENV PYLOAD_PASSWORD=XXX

COPY requirements.txt .
COPY app.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py" ]