FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir httpx==0.27.2

COPY main.py /app/main.py
COPY AGENT.md /app/AGENT.md
COPY personas.json /app/personas.json
# anet.chat v14: condensed in-tree persona files (was: bind-mounted from refs/<slug>-skill).
# Each ~3-4KB; only 心智模型 + 表达 DNA + 信号词汇 + 反模式 + 白板行为 kept.
COPY personas/ /app/personas/

ENV PYTHONUNBUFFERED=1
ENV PERSONAS_REGISTRY=/app/personas.json
ENV AGENT_MD=/app/AGENT.md

CMD ["python", "-u", "/app/main.py"]
