# TickPay API Quickstart 🚀

Welcome to the **TickPay Developer Network**. 

TickPay provides a seamless, institutional-grade API designed to connect Autonomous AI Agents and microservices to our financial settlement network. This repository contains the essential tools, boilerplate code, and documentation to initialize your integration securely.

## 🔒 Authentication & Zero-Trust Guidelines

TickPay operates under a strict Zero-Trust architectural model. To authenticate your AI Agents, you must provision cryptographic API Keys directly from your production portal.

**How to get your API Key:**
1. Log in to your TickPay Dashboard at [https://tickpay.dev/login](https://tickpay.dev/login).
2. Navigate to the sidebar menu and select **Settings** (Configuraciones).
3. Click the **Generate API Key** button.
4. Copy your newly forged key (it will begin with `sk_live_...`) and store it securely in your local environment. *You will only see this key once.*

**CRITICAL COMPLIANCE RULES:**
1. **Never hardcode your API Key:** The `TICKPAY_API_KEY` must **never** be hardcoded in your source files or committed to any version control system (e.g., GitHub, GitLab).
2. **Use Environment Variables:** Always inject your credentials via a `.env` file or your CI/CD secrets manager.
3. **Authorization Header:** All requests to our network must include the standard HTTP authorization header containing your API token:
   ```http
   Authorization: Bearer <YOUR_API_KEY>
   ```

*Failure to secure your keys may result in immediate, automated cryptographic revocation of your Agent's access.*

## 🔌 API Endpoint Topology

The TickPay API is served strictly over TLS 1.3 at our primary production origin.

- **Base URL:** `https://tickpay.dev/v1`
- **Format:** JSON (`application/json`)
- **Rate Limits:** Enforced dynamically per Agent identity configuration.

## 🚀 Getting Started (Examples)

We provide reference implementations in standard backend languages for immediate onboarding. Ensure you have your testing API key (e.g., `tkp_live_xxxxxxxx`) handy.

1. **[Node.js (JavaScript)](./examples/node-agent.js):** Connect your Node-based Agent to register quiz completion rewards. (Uses `axios` or native `fetch`).
2. **[Python](./examples/python-agent.py):** Execute automated royalty dispersals via your Python automation daemon. (Uses `requests`).

## 📖 Payload Parameters Dictionary

When crafting your transaction intents, ensure your Agent sends the following strictly typed JSON parameters to the `/transactions/intent` endpoint:

| Parameter | Type | Required | Example | Description |
| :--- | :--- | :--- | :--- | :--- |
| `amount` | Integer / Float | Yes | `50`, `1.50` | The exact physical or tokenized amount to transfer. |
| `currency` | String | Yes | `"USD"`, `"TKP"` | The fiat or digital currency ticker for the settlement. |
| `recipientId` | String | Yes | `"usr_creator_ai_101"`| The unique internal identifier of the destination recipient. |
| `transactionType` | String | Yes | `"reward"`, `"royalty"` | The semantic classification of the transaction logic. |

---
*TickPay — Engineered for the Algorithmic Economy.*
