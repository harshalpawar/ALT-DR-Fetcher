import requests
import sys
import os
import json
from dotenv import load_dotenv
from tqdm import tqdm  # Add tqdm import

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Load brand dictionary from JSON file
brand_list_path = os.path.join(os.path.dirname(__file__), 'data', 'brand_list.json')
with open(brand_list_path, 'r') as f:
    brand_dict = json.load(f)['brands']

# Select a brand dynamically
brand_name = sys.argv[1] if len(sys.argv) > 1 else "Levi's"  # Use command line argument or default
brand = next((b for b in brand_dict if b["name"] == brand_name), None)

# Check if brand exists, otherwise exit
if not brand:
    print(f"❌ Brand '{brand_name}' not found in brand_dict. Exiting...")
    sys.exit(1)  # Exit program with an error code

# Define the output file path for the brand's links
brand_json_path = brand.get("localPath")

if not brand_json_path or not os.path.exists(brand_json_path):
    print(f"❌ Brand JSON file not found for {brand_name}")
    sys.exit(1)

# Read the existing brand JSON file
with open(brand_json_path, 'r', encoding='utf-8') as f:
    brand_data = json.load(f)

# Prepare API headers
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {JINA_API_KEY}',
    'X-Md-Link-Style': 'referenced',
    'X-Retain-Images': 'none',
    'X-Return-Format': 'text',
    'X-With-Images-Summary': 'all',
    'X-With-Links-Summary': 'all'
}

# Initialize page_text list if not exists
if 'page_text' not in brand_data:
    brand_data['page_text'] = []

# Filter out already processed links
unprocessed_links = [
    link for link in brand_data['links'] 
    if not any(existing.get('url') == link['url'] for existing in brand_data['page_text'])
]

# Process each link with tqdm
for link in tqdm(unprocessed_links, desc=f"Processing {brand_name} links", unit="link"):
    try:
        # Query the API for the link
        response = requests.get(f'https://r.jina.ai/{link["url"]}', headers=headers)
        
        # Parse the JSON response
        response_json = response.json()
        
        # Prepare the response data
        response_data = {
            'url': link['url'],
            'title': link['title'],
            'content': response_json['data']['text']  # Extract the text content
        }
        
        # Append to page_text list
        brand_data['page_text'].append(response_data)
    
    except (KeyError, json.JSONDecodeError) as e:
        # Optionally, add an error entry
        error_data = {
            'url': link['url'],
            'title': link['title'],
            'content': f'Error extracting content: {str(e)}'
        }
        brand_data['page_text'].append(error_data)
    except Exception as e:
        print(f"Unexpected error processing {link['url']}: {e}")

# Save the updated brand data
with open(brand_json_path, 'w', encoding='utf-8') as f:
    json.dump(brand_data, f, indent=2)

print(f"Updated {brand_name} data file with API responses")
print(f"Total links processed: {len(brand_data['page_text'])}")