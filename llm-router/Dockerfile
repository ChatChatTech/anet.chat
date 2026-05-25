FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir httpx==0.27.2 fastapi==0.115.0 uvicorn==0.30.6
COPY main.py /app/main.py
ENV PYTHONUNBUFFERED=1
EXPOSE 4860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4860"]
