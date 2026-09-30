"""Read-only deployment checks for SamiSaverBot.

This script validates credentials without sending Telegram messages, changing the
webhook, or starting a polling worker.
"""

import os
import sys

import requests

from aliexpress_api import AliexpressApi, models


def required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    token = required("TELEGRAM_BOT_TOKEN")
    api_key = required("ALIEXPRESS_API_PUBLIC")
    api_secret = required("ALIEXPRESS_API_SECRET")

    response = requests.get(
        f"https://api.telegram.org/bot{token}/getMe",
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    identity = payload.get("result", {})
    if payload.get("ok") is not True or identity.get("username", "").casefold() != "samisaverbot":
        raise RuntimeError("Telegram token does not belong to @SamiSaverBot")

    # Construction exercises the bundled SDK and confirms the deployment has all
    # required configuration. It does not create affiliate links or mutate state.
    AliexpressApi(
        api_key,
        api_secret,
        models.Language.AR,
        models.Currency.EUR,
        "telegramBot",
    )

    print("Telegram identity: @SamiSaverBot")
    print("AliExpress client: initialized")
    print("Smoke test: PASS (no messages sent; webhook unchanged)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        # Do not print request URLs because Telegram API URLs contain the token.
        print(f"Smoke test: FAIL ({type(error).__name__})", file=sys.stderr)
        raise SystemExit(1) from None
