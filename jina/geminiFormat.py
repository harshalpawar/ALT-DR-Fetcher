# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv
from paths import BRAND_LIST_FILE, ENV_FILE

# Load environment variables from parent directory
load_dotenv(ENV_FILE)

def getBrand(brand_name):
    # Load brand dictionary from JSON file
    with open(BRAND_LIST_FILE, 'r') as f:
        brand_dict = json.load(f)['brands']

    brand = next((b for b in brand_dict if b["name"] == brand_name), None)
    return brand

def getResponse(brand):
    if brand is None:
        print(f"❌ Brand not found")
        return None

    if not brand['localPath'] or not os.path.exists(brand['localPath']):
        print(f"❌ Brand JSON file not found for {brand['name']}")
        return None

    # Read the brand's JSON file
    with open(brand['localPath'], 'r', encoding='utf-8') as f:
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
    - Estimated Delivery Time: Within B days OR A-B days (if a range is specified)

    **Returns:**
    - Return Period: X days
    - Return Method: Brand pickup / Self-ship **Mention the return pickup charges if any**.
    - Refund Mode: Bank a/c / Store credit / Other

    🔹 **Important Simplification Rules:**
    - **Delivery Charges:** If there is a free shipping threshold, write as: "Delivery Charges: Rs. X; Free over Rs. Y".
    - **Return Methods:**
    - If the brand arranges a pickup, even if they use terms like **"scheduled courier pickup" or "reverse logistics service"**, treat it as **"Brand pickup"**. **Mention the return pickup charges if any**.
    - If the customer **must ship the item themselves** using their own courier or by dropping it at a store/courier location, classify it as **"Self-ship"**.
    - If returns are **only for exchanges**, format as: "X days - exchanges only". If exchanges are size only, then mention it as "X days - exchanges only (size only)".
    - **Refund Mode:** If refunds are to a bank account, state "Refund in bank a/c". If store credit is used, state "Refund as store credit".
    - **No unnecessary details** should be included. Keep only what's relevant.
    - Do **not** make up information—return 'Not specified' for missing details.

    Ensure **clarity and structured formatting** as per the above rules.
    """

    # Prepare the user prompt
    user_prompt = f"""Extract the delivery and return policy for {brand['name']} from the following web page contents:

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
    # Update the brand's entry in brand_list.json with the Gemini response
    try:
        with open(BRAND_LIST_FILE, 'r', encoding='utf-8') as f:
            brand_list = json.load(f)
        
        for brand_entry in brand_list['brands']:
            if brand_entry['name'] == brand['name']:
                brand_entry['response'] = response.text
                break
        
        with open(BRAND_LIST_FILE, 'w', encoding='utf-8') as f:
            json.dump(brand_list, f, indent=4)
        
        print(f"Updated brand_list.json with Gemini response for {brand['name']}")

    except Exception as e:
        print(f"Error updating brand_list.json with Gemini response: {e}")

def main():
    brand_name = ""
    brand = getBrand(brand_name)
    getResponse(brand)

if __name__ == "__main__":
    main() 
