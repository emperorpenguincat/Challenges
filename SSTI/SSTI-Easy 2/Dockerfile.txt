FROM python:3.10-slim

WORKDIR /sstichall

RUN useradd -m sstichall

RUN pip install --no-cache-dir flask

COPY . .

RUN chown -R sstichall:sstichall /sstichall

USER sstichall

EXPOSE 5000

CMD ["python", "app.py"]
