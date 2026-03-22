"""WhatsApp Cloud API - Flask Application with Webhook Handler."""

import asyncio
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from whatsapp_client import WhatsAppClient
from webhook_handler import (
    validate_hmac_signature,
    verify_webhook,
    parse_webhook_payload,
    extract_message_content,
)

load_dotenv()

app = Flask(__name__)

# Initialize WhatsApp client
whatsapp = WhatsAppClient()


# === Webhook Routes ===


@app.route("/webhook", methods=["GET"])
def webhook_verify():
    """Handle webhook verification (GET challenge from Meta)."""
    return verify_webhook()


@app.route("/webhook", methods=["POST"])
@validate_hmac_signature()
def webhook_receive():
    """Handle incoming messages and status updates."""
    data = request.get_json()

    # Parse webhook payload
    parsed = parse_webhook_payload(data)

    # Process messages
    for message in parsed["messages"]:
        asyncio.run(handle_incoming_message(message))

    # Process status updates
    for status in parsed["statuses"]:
        handle_status_update(status)

    # Always return 200 within 5 seconds
    return "OK", 200


# === Message Handler ===


async def handle_incoming_message(message: dict) -> None:
    """Process an incoming message and send a response."""
    from_number = message["from"]
    content = extract_message_content(message)

    print(f"Message from {from_number}: [{content['type']}] {content.get('text', '')}")

    # Mark as read
    await whatsapp.mark_as_read(message["id"])

    # TODO: Implement your message handling logic here
    # Example: Echo back the message
    match content["type"]:
        case "text":
            await whatsapp.send_text(from_number, f"Recebi sua mensagem: \"{content['text']}\"")

        case "button":
            await whatsapp.send_text(from_number, f"Voce selecionou: {content['text']}")

        case "list":
            await whatsapp.send_text(from_number, f"Voce escolheu: {content['text']}")

        case "image" | "document" | "video" | "audio":
            await whatsapp.send_text(from_number, f"Recebi sua midia ({content['type']}).")

        case _:
            await whatsapp.send_text(from_number, "Desculpe, nao entendi. Como posso ajudar?")


# === Status Handler ===


def handle_status_update(status: dict) -> None:
    """Process a message status update."""
    print(f"Status update: {status['id']} -> {status['status']}")

    if status["status"] == "failed":
        errors = status.get("errors", [])
        print(f"Message delivery failed: {errors}")


# === Health Check ===


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


# === Start Server ===

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print(f"WhatsApp webhook server running on port {port}")
    print(f"Webhook URL: http://localhost:{port}/webhook")
    print(f"Health check: http://localhost:{port}/health")
    app.run(host="0.0.0.0", port=port, debug=True)
