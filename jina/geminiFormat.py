from google import genai
from google.genai import types
import os
import json
import sys
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Load brand dictionary from JSON file
brand_list_path = os.path.join(os.path.dirname(__file__), 'data', 'brand_list.json')
with open(brand_list_path, 'r') as f:
    brand_dict = json.load(f)['brands']

# Select a brand dynamically
brand_name = "Levi's"  # Change this to the brand you want
brand = next((b for b in brand_dict if b["name"] == brand_name), None)

# Check if brand exists, otherwise exit
if not brand:
    print(f"❌ Brand '{brand_name}' not found in brand_dict. Exiting...")
    sys.exit(1)  # Exit program with an error code

# Get the local path of the brand's JSON file
brand_json_path = brand.get("localPath")

if not brand_json_path or not os.path.exists(brand_json_path):
    print(f"❌ Brand JSON file not found for {brand_name}")
    sys.exit(1)

# Read the brand's JSON file
with open(brand_json_path, 'r', encoding='utf-8') as f:
    brand_data = json.load(f)

# Combine all page_text content into a single string
content_prompt = "\n\n".join([
    f"URL: {item['url']}\nTitle: {item['title']}\nContent: {item['content']}" 
    for item in brand_data.get('page_text', [])
])

# Get API key from environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

# Prepare the user prompt
user_prompt = f"""Extract the delivery and return policy for {brand_name} from the following web page contents:

{content_prompt}

Follow the response format and simplification rules strictly."""

# Generate content
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    config=types.GenerateContentConfig(
        system_instruction=system_prompt
    ),
    contents=user_prompt
)

# Print the response
print(response.text)