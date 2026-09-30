# SamiSaverBot operations

## Runtime

The DigitalOcean deployment uses Telegram long polling. It exposes no inbound
port and does not require a domain or TLS certificate. The container is limited
to 160 MiB RAM and half a CPU so it can coexist with the existing workers.

Required secrets live only in `/opt/samisaver-bot/.env` on the VPS:

- `TELEGRAM_BOT_TOKEN`
- `ALIEXPRESS_API_PUBLIC`
- `ALIEXPRESS_API_SECRET`

Never commit that file. `WEBHOOK_URL` is forced empty by `compose.yaml`.

## Preflight

```sh
docker compose build
docker compose run --rm --no-deps samisaver python smoke_test.py
```

The smoke test calls Telegram `getMe` and initializes the AliExpress SDK. It
does not send a message, alter the webhook, or start polling.

## Cutover

Starting the container removes the old Render webhook and begins polling:

```sh
docker compose up -d
docker compose ps
docker compose logs --tail=100 samisaver
```

After a successful Telegram `/start` and product-link test, suspend the Render
service `AliexpressRenderBot`. The Render PostgreSQL database is not referenced
by this application; confirm no other service is attached before deleting it.

## Rollback to Render

Stop the VPS worker first, then restore the known Render webhook:

```sh
docker compose stop samisaver
set -a
. ./.env
set +a
curl --fail --silent --show-error \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  --data-urlencode "url=https://aliexpressrenderbot.onrender.com/webhook"
```

Verify rollback with Telegram `getWebhookInfo`. Do not print or paste the bot
token into logs or chat.
