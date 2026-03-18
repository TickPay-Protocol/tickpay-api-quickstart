"""
TickPay Python Integration Agent
Scenario: Nexus-Audio-AI dispersing a $1.50 USD micro-payment to a creator for an AI-generated audio sample usage.
"""

import os
import sys
import uuid
import requests
from dotenv import load_dotenv

# Load environment configuration securely
load_dotenv()

# Enforce Zero-Trust configuration
TICKPAY_API_KEY = os.getenv("TICKPAY_API_KEY")

if not TICKPAY_API_KEY:
    print("FATAL: TICKPAY_API_KEY environment variable is missing.")
    print("Please secure your credentials within a .env file (e.g., TICKPAY_API_KEY=tkp_live_xxxxxxxx).")
    sys.exit(1)

# TickPay Production Origin
TICKPAY_BASE_URL = "https://tickpay.dev/v1"

def disperse_royalties():
    print("Initializing Agent connection to TickPay Network...")

    # Transaction metadata
    payload = {
        "amount": 1.50,
        "currency": "USD",
        "reference": "NEXUS_AUDIO_SAMPLE_USAGE_001",
        "description": "Automatic micro-payment for AI-generated audio sample usage",
        "recipientId": "usr_creator_ai_101"
    }

    headers = {
        "Authorization": f"Bearer {TICKPAY_API_KEY}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": f"etr_{uuid.uuid4()}" # Essential for guaranteed exactly-once processing
    }

    try:
        # Connect to the TickPay origin endpoint
        response = requests.post(
            f"{TICKPAY_BASE_URL}/transactions/intent",
            json=payload,
            headers=headers,
            timeout=5.0
        )

        # Raise an exception for HTTP error codes
        response.raise_for_status()

        data = response.json()
        print(f"✅ [SUCCESS] Micro-payment Authorized. ID: {data.get('id', 'Pending')}")
        print(f"    Amount: ${payload['amount']} {payload['currency']}")

    except requests.exceptions.HTTPError as e:
        print(f"❌ [HTTP ERROR] Refused by TickPay Firewall: {e.response.status_code}")
        print(f"Details: {e.response.text}")
    except requests.exceptions.Timeout:
        print("❌ [TIMEOUT ERROR] TickPay TLS connection timed out.")
    except requests.exceptions.RequestException as e:
        print(f"❌ [CRITICAL ERROR] Execution failed: {str(e)}")

if __name__ == "__main__":
    disperse_royalties()
