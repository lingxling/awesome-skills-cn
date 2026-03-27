#!/usr/bin/env python3
"""
Send a test message via WhatsApp Cloud API.

Quick way to validate your setup by sending a text message.

Usage:
    python send_test_message.py --to 5511999999999 --message "Hello from WhatsApp API!"
    python send_test_message.py --to 5511999999999  # Uses default test message
"""

import argparse
import os
import sys

try:
    import httpx
except ImportError:
    print("Error: httpx not installed. Run: pip install httpx")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

GRAPH_API = "https://graph.facebook.com/v21.0"


def _mask_secret(value: str) -> str:
    """Return a masked version of a secret for safe logging."""
    if not value or len(value) < 8:
        return "***masked***"
    return f"{value[:6]}...masked"


def send_test(to: str, message: str) -> None:
    """Send a test text message."""
    token = os.environ.get("WHATSAPP_TOKEN")
    phone_id = os.environ.get("PHONE_NUMBER_ID")

    if not token or not phone_id:
        print("Error: WHATSAPP_TOKEN and PHONE_NUMBER_ID must be set.")
        print("Configure your .env file or set environment variables.")
        sys.exit(1)

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message},
    }

    print(f"Sending message to: {to}")
    print(f"Message: {message}")
    print()

    try:
        response = httpx.post(
            f"{GRAPH_API}/{phone_id}/messages",
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

        data = response.json()

        if response.status_code == 200:
            msg_id = data.get("messages", [{}])[0].get("id", "N/A")
            print("Message sent successfully!")
            print(f"  Message ID: {msg_id}")
            print(f"  Status: 200 OK")
        else:
            error = data.get("error", {})
            print(f"Error sending message:")
            print(f"  Code: {error.get('code', '?')}")
            print(f"  Status: {response.status_code}")
            print("  Message: Request rejected by WhatsApp Cloud API.")

        print()
        print("Response details omitted to avoid exposing sensitive API data.")

    except httpx.ConnectError:
        print("Error: Connection failed. Check your internet connection.")
        sys.exit(1)
    except httpx.TimeoutException:
        print("Error: Request timed out.")
        sys.exit(1)
    except Exception:
        print("Error: Unexpected failure while sending the message.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Send a test WhatsApp message")
    parser.add_argument(
        "--to",
        required=True,
        help="Recipient phone number with country code (e.g., 5511999999999)",
    )
    parser.add_argument(
        "--message",
        default="Teste de integracao WhatsApp Cloud API - Mensagem enviada com sucesso!",
        help="Message text to send",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file (default: .env)",
    )

    args = parser.parse_args()

    # Load environment
    if load_dotenv:
        for env_path in [args.env_file, os.path.join(os.getcwd(), ".env")]:
            if os.path.exists(env_path):
                load_dotenv(env_path)
                break

    send_test(args.to, args.message)


if __name__ == "__main__":
    main()
