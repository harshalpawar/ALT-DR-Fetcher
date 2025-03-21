# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import requests
import os
import json
from dotenv import load_dotenv
from tqdm import tqdm  # Add tqdm import
from paths import BRAND_LIST_FILE, ENV_FILE
from utils import getBrand

# Load environment variables from parent directory
load_dotenv(ENV_FILE)

def getFormattedWebpage(brand):
    if brand is None:
        print(f"❌ Brand not found")
        return None

    if not brand['localPath'] or not os.path.exists(brand['localPath']):
        print(f"❌ Brand JSON file not found for {brand['name']}")
        return None
 
    # Read the brand's JSON file
    with open(brand['localPath'], 'r', encoding='utf-8') as f:
        brand_data = json.load(f)

    # Ensure 'page_text' key exists, initializing if not present
    if 'page_text' not in brand_data:
        brand_data['page_text'] = []

    JINA_API_KEY = os.getenv("JINA_API_KEY")
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

    # Filter out already processed links
    unprocessed_links = [
        link for link in brand_data['links'] 
        if not any(existing.get('url') == link['url'] for existing in brand_data['page_text'])
    ]

    # Process each link with tqdm
    for link in tqdm(unprocessed_links, desc=f"Processing {brand['name']} links", unit="link"):
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
    with open(brand['localPath'], 'w', encoding='utf-8') as f:
        json.dump(brand_data, f, indent=2)

    print(f"Updated {brand['name']} data file with API responses")
    print(f"Total links processed: {len(brand_data['page_text'])}")

def main():
    brand_name = ""
    brand = getBrand(brand_name)
    getFormattedWebpage(brand)
if __name__ == "__main__":
    main() 