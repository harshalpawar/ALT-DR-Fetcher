import requests
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Define the brand dictionary
brand_dict = [ 
    {"name": "H&M", "url": "hm.com/in"},
    {"name": "Zara", "url": "zara.com/in/"},
    {"name": "Nike", "url": "nike.com/in/"},
    {"name": "Adidas", "url": "adidas.co.in/"},
    {"name": "Levi's", "url": "levi.in/"},
    {"name": "Myntra", "url": "myntra.com/"},
    {"name": "Ajio", "url": "ajio.com/"},
    {"name": "Uniqlo", "url": "uniqlo.com/in/en/"},
    {"name": "Snitch", "url": "snitch.com"},
]

# Select a brand dynamically
brand_name = "Levi's"  # Change this to the brand you want
brand = next((b for b in brand_dict if b["name"] == brand_name), None)

# Check if brand exists, otherwise exit
if not brand:
    print(f"❌ Brand '{brand_name}' not found in brand_dict. Exiting...")
    sys.exit(1)  # Exit program with an error code

url = 'https://s.jina.ai/?q=return+exchange+delivery+shipping+pickup+refund&gl=IN&location=Mumbai&hl=en'
headers = {
    'Authorization': f'Bearer {JINA_API_KEY}',
    'X-Site': brand["url"],
    'X-With-Links-Summary': 'true'
}

response = requests.get(url, headers=headers)

# Dump the response to a text file
with open('jina_dump.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("response saved to jina_dump.txt")