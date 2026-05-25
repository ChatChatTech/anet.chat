FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir httpx==0.27.2

COPY main.py /app/main.py
COPY AGENT.md /app/AGENT.md
COPY personas.json /app/personas.json

ENV PYTHONUNBUFFERED=1
ENV PERSONAS_REGISTRY=/app/personas.json
ENV AGENT_MD=/app/AGENT.md

CMD ["python", "-u", "/app/main.py"]
