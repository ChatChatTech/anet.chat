FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir httpx==0.27.2
COPY main.py /app/main.py
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "/app/main.py"]
