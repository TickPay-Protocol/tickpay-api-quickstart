/**
 * TickPay Node.js Integration Agent
 * Scenario: AutoDev-Bot disbursing a 50-token reward to a human for solving a visual training captcha.
 */

require('dotenv').config();
const axios = require('axios'); // Note: You can also use native fetch in Node 18+

// Enforce Zero-Trust configuration
const TICKPAY_API_KEY = process.env.TICKPAY_API_KEY;

if (!TICKPAY_API_KEY) {
    console.error("FATAL: TICKPAY_API_KEY environment variable is not set.");
    console.error("Please configure your .env file securely (e.g., TICKPAY_API_KEY=tkp_live_xxxxxxxx).");
    process.exit(1);
}

// TickPay Production Origin
const TICKPAY_BASE_URL = 'https://tickpay.dev/v1';

async function registerQuizReward() {
    console.log("Initializing Agent connection to TickPay Network...");

    // Payload representing the transaction intent
    const payload = {
        amount: 50,
        currency: "TKP", // TickPay Platform Tokens
        reference: "AUTODEV_CAPTCHA_SOLVE_9821A",
        description: "Reward dispersal for visual training captcha solved by human operator",
        recipientId: "usr_998ab2192" // Target recipient identifier
    };

    try {
        const response = await axios.post(`${TICKPAY_BASE_URL}/transactions/intent`, payload, {
            headers: {
                'Authorization': `Bearer ${TICKPAY_API_KEY}`,
                'Content-Type': 'application/json',
                'X-Idempotency-Key': `tqz_${Date.now()}` // Best practice for deduplication
            },
            timeout: 5000 // 5 seconds SLA
        });

        console.log(`✅ [SUCCESS] Transaction Intent Registered: ${response.data.id || 'Pending'}`);
        console.log(`Status: ${response.status}`);
        
    } catch (error) {
        console.error("❌ [ERROR] TickPay Network Communication Failed.");
        
        if (error.response) {
            // The server responded with a status code outside the 2xx range (e.g. 401 Unauthorized, 403 Forbidden)
            console.error(`Status Code: ${error.response.status}`);
            console.error(`TickPay Response:`, error.response.data);
        } else if (error.request) {
            // The request was made but no response was received (Timeout/Network)
            console.error("No response received from TickPay origins. Verify network connectivity.");
        } else {
            console.error("Agent Execution Error:", error.message);
        }
    }
}

// Execute routine
registerQuizReward();
