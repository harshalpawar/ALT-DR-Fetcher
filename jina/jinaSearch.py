import requests
import sys
import os
import json
from dotenv import load_dotenv

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
output_file = os.path.join(os.path.dirname(__file__), 'data', 'brands', f'{brand["name"]}_data.json')

urlDelivery = "https://s.jina.ai/?q=delivery+shipping+terms+policy+faq+help&gl=IN&location=Mumbai&hl=en"
urlReturn = "https://s.jina.ai/?q=returns+refund+exchange+pickup+terms+policy+faq+help&gl=IN&location=Mumbai&hl=en"
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {JINA_API_KEY}",
    "X-Respond-With": "no-content",
    "X-Site": brand["url"]
}

responseDelivery = requests.get(urlDelivery, headers=headers)
responseReturn = requests.get(urlReturn, headers=headers)

# Parse the JSON responses
try:
    # Parse both responses
    response_data_delivery = responseDelivery.json()
    response_data_return = responseReturn.json()
    
    # Extract URLs and titles from both responses
    filtered_data_delivery = [
        {
            "url": item["url"],
            "title": item["title"]
        } for item in response_data_delivery.get("data", [])
    ]
    
    filtered_data_return = [
        {
            "url": item["url"],
            "title": item["title"]
        } for item in response_data_return.get("data", [])
    ]
    
    # Combine and remove duplicates
    combined_data = filtered_data_delivery + filtered_data_return
    unique_data = []
    seen_urls = set()
    
    for item in combined_data:
        if item['url'] not in seen_urls:
            unique_data.append(item)
            seen_urls.add(item['url'])
    
    # Save unique filtered data to a JSON file in the brand-specific folder
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"links": unique_data}, f, indent=2)
    # Update the brand's entry in brand_list.json with the local path of the links file
    try:
        with open(brand_list_path, 'r', encoding='utf-8') as f:
            brand_list = json.load(f)
        
        for brand_entry in brand_list['brands']:
            if brand_entry['name'] == brand['name']:
                brand_entry['localPath'] = output_file
                break
        
        with open(brand_list_path, 'w', encoding='utf-8') as f:
            json.dump(brand_list, f, indent=4)
        
        print(f"Updated brand_list.json with local path for {brand['name']}")
    
    except Exception as e:
        print(f"Error updating brand_list.json: {e}")
    print(f"Unique links for {brand['name']} saved to {output_file}")
    print(f"Total unique links: {len(unique_data)}")

except json.JSONDecodeError:
    print("Error: Unable to parse JSON response")
    # Dump the raw responses for debugging
    with open('error_delivery_dump.txt', 'w', encoding='utf-8') as f:
        f.write(responseDelivery.text)
    with open('error_return_dump.txt', 'w', encoding='utf-8') as f:
        f.write(responseReturn.text)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)