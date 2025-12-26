FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY api.py /app/api.py
COPY static /app/static

EXPOSE 8000

# Many hosts set $PORT (Render/Railway/etc.). Default to 8000.
CMD ["bash", "-lc", "python -m uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]

