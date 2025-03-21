import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Initialize Perplexity API Client
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# Load extracted text 
with open("jina_dump.txt", "r", encoding="utf-8") as file:
    policy_text = file.read()

# Define System Prompt
system_prompt = """Your purpose is to extract the delivery and return policy of a fashion brand in India.

📌 **RESPONSE FORMAT (Strictly follow this structure):**
**Delivery:**
- Delivery Charges: Rs. X; Free over Rs. Y (or "Free shipping" if applicable)
- Estimated Delivery Time: A-B days

**Returns:**
- Return Period: X days
- Return Method: Brand pickup / Self-ship **Mention the return pickup charges if any**.
- Refund Mode: Bank a/c / Store credit / Other

🔹 **Important Simplification Rules:**
- **Delivery Charges:** If there is a free shipping threshold, write as: "Delivery Charges: Rs. X; Free over Rs. Y".
- **Delivery Time:** If metro and non-metro times are different, merge them into a single range (e.g., "2-5 days" + "5-7 days" → "2-7 days").
- **Return Methods:**
  - If the brand arranges a pickup, even if they use terms like **"scheduled courier pickup" or "reverse logistics service"**, treat it as **"Brand pickup"**. **Mention the return pickup charges if any**.
  - If the customer **must ship the item themselves** using their own courier or by dropping it at a store/courier location, classify it as **"Self-ship"**.
  - If returns are **only for exchanges**, format as: "X days - exchanges only; Self-ship".
- **Refund Mode:** If refunds are to a bank account, state "Refund in bank a/c". If store credit is used, state "Refund as store credit".
- **No unnecessary details** should be included. Keep only what's relevant.
- Do **not** make up information—return 'Not specified' for missing details.

Ensure **clarity and structured formatting** as per the above rules.
"""

# Define User Prompt (Pass extracted text instead of a query)
user_prompt = f"""Format the following text into the structured response format:\n\n{policy_text}"""


# Define settings
settings = {
    "model": "sonar-pro",  # Best model for factual search
    "temperature": 0.1,  # Keep responses deterministic and factual
    "max_tokens": 500,  # Ensure responses are long enough but controlled
    "top_p": 0.3,  # Reduce randomness
    "frequency_penalty": 0,  # Avoid unnecessary word repetition
    "presence_penalty": 0,  # Allow all relevant details to appear
#    "search_recency_filter": "week",  # Get the most recent policies
#    "search_domain_filter": [brand["url"]],  # Can be set to ["hm.com", "zara.com"] for accuracy
#    "web_search_options": {"search_context_size": "high"}  # Ensure deeper context from web results
}
# Make API call
response = client.chat.completions.create(
    **settings,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
)

# Print response
print("✅ API Call Successful!\n")
print("🔍 Structured Response:\n", response.choices[0].message.content)
