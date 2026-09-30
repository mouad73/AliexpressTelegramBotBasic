FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system bot && adduser --system --ingroup bot bot

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY --chown=bot:bot Bot.py ./
COPY --chown=bot:bot aliexpress_api ./aliexpress_api
COPY --chown=bot:bot smoke_test.py ./

USER bot

CMD ["python", "Bot.py"]
