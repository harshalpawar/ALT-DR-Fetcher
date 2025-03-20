import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Initialize Perplexity API Client
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# Brand details dictionary
brand = {
    "name": "H&M",
    "url": "https://www2.hm.com/en_in/index.html"
}

# Define settings
settings = {
    "model": "sonar-pro",  # Best model for factual search
#    "num_results": 8,  # Fetch data from x sources for maximum accuracy
    "temperature": 0.1,  # Keep responses deterministic and factual
    "max_tokens": 500,  # Ensure responses are long enough but controlled
    "top_p": 0.3,  # Reduce randomness
    "frequency_penalty": 0,  # Avoid unnecessary word repetition
    "presence_penalty": 0,  # Allow all relevant details to appear
#    "search_recency_filter": "week",  # Get the most recent policies
#    "search_domain_filter": [],  # Can be set to ["hm.com", "zara.com"] for accuracy
    "web_search_options": {"search_context_size": "high"}  # Ensure deeper context from web results
}
# System prompt as a single string (easy to edit)
system_prompt = """Your purpose is to extract the delivery and return policy of a fashion brand in India.

📌 **RESPONSE FORMAT (Strictly follow this structure):**
**Delivery:**
- Delivery Charges: (Free / Free above Rs. X / Standard rate Rs. Y)
- Estimated Delivery Time: (Range of days)

**Returns:**
- Return Period: (X days)
- Return Method: (Self-shipping / In-store return / Brand pickup)
- Refund Mode: (Bank account / Brand wallet / Store credit)

**Additional Information:**
List any relevant policies not covered above, such as exchange policies, late return fees, 
restocking fees, membership benefits, special conditions, or return restrictions.

🔹 **Important Notes:**
- Extract only **factual details** from official sources.
- If multiple policies exist (e.g., COD vs. prepaid), specify both.
- If the **brand URL does not provide full info**, supplement using the best available web sources.
- Do **not** make up information—return 'Not specified' for missing details.
- Ensure **clarity and structured formatting**."""



# User prompt as a single string (also easy to edit)
user_prompt = f"""Find me the latest return and delivery policy of {brand["name"]} from {brand["url"]} in India. 
Prioritize the official website ({brand["url"]}), but if details are missing, check other reliable sources. 
Follow the response format strictly and include an 'Additional Information' section for anything useful 
that doesn't fit into the standard categories."""

# Define messages
messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt
    },
]

# Make API call (Non-streaming response)
response = client.chat.completions.create(
    **settings,
    messages=messages
)

# Assuming you're working with an API response object (like from OpenAI, Anthropic, etc.)
final_answer = response.choices[0].message.content
full_choice = response.choices[0]
token_usage = response.usage
citations = response.choices[0].citations if hasattr(response.choices[0], 'citations') else None

# Timestamp for this API call
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Output to a text file
output_file = 'api_response_log.txt'
with open(output_file, 'a', encoding='utf-8') as f:
    # Add a separator between log entries
    f.write("\n" + "="*50 + "\n")
    f.write(f"API Call Timestamp: {timestamp}\n")
    f.write("="*50 + "\n\n")
    
    # Write settings with clear formatting
    f.write("API Request Settings:\n")
    for key, value in settings.items():
        f.write(f"  {key.ljust(20)}: {value}\n")
    
    # Write prompts with clear formatting
    f.write("\nSystem Prompt:\n")
    f.write(f"{system_prompt}\n")
    
    f.write("\nUser Prompt:\n")
    f.write(f"{user_prompt}\n")
    
    # Detailed response logging
    f.write("\nResponse Details:\n")
    f.write(f"  Final Answer       : {final_answer}\n")
    f.write(f"  Token Usage       : {token_usage}\n")
    
    # Safely handle citations
    if hasattr(response.choices[0], 'citations') and response.choices[0].citations:
        f.write("  Citations         :\n")
        for citation in response.choices[0].citations:
            f.write(f"    - {citation}\n")
    else:
        f.write("  Citations         : None\n")

# Also print to console for immediate feedback
print(f"Response details appended to {output_file}")
print(f"Timestamp: {timestamp}")
print("Final Answer:", final_answer)
print("Full Choice:", full_choice)
