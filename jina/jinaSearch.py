# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import requests
import sys
import os
import json
from dotenv import load_dotenv
from paths import BRAND_LIST_FILE, ENV_FILE, BRANDS_DIR, JINA_DIR
from utils import getBrand

# Load environment variables from parent directory
load_dotenv(ENV_FILE)

def search(brand):
    if brand is None:
        print(f"❌ Brand not found")
        return None
    
    # Define the output file path for the brand's links
    output_file = os.path.join(BRANDS_DIR, f'{brand["name"]}_data.json')
    JINA_API_KEY = os.getenv("JINA_API_KEY")
    urlDelivery = f"https://s.jina.ai/?q=delivery+shipping+charges&gl=IN&location=Mumbai&hl=en"
    urlReturn = f"https://s.jina.ai/?q=returns+refund&gl=IN&location=Mumbai&hl=en"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {JINA_API_KEY}",
        "X-Respond-With": "no-content",
        "X-Site": brand["url"]
    }
    print(brand)
    responseDelivery = requests.get(urlDelivery, headers=headers)
    responseReturn = requests.get(urlReturn, headers=headers)
    print(responseDelivery.text)
    print(responseReturn.text)
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
            with open(BRAND_LIST_FILE, 'r', encoding='utf-8') as f:
                brand_list = json.load(f)
            
            for brand_entry in brand_list['brands']:
                if brand_entry['name'] == brand['name']:
                    brand_entry['localPath'] = output_file
                    break
            
            with open(BRAND_LIST_FILE, 'w', encoding='utf-8') as f:
                json.dump(brand_list, f, indent=4)
            
            print(f"Updated brand_list.json with local path for {brand['name']}")
        
        except Exception as e:
            print(f"Error updating brand_list.json: {e}")
        print(f"Unique links for {brand['name']} saved to {output_file}")
        print(f"Total unique links: {len(unique_data)}")

    except json.JSONDecodeError:
        print("Error: Unable to parse JSON response")
        # Dump the raw responses for debugging
        error_dump_path = os.path.join(JINA_DIR, 'data', 'error_delivery_dump.txt')
        with open(error_dump_path, 'w', encoding='utf-8') as f:
            f.write(responseDelivery.text)
        with open(error_dump_path, 'a', encoding='utf-8') as f:
            f.write(responseReturn.text)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    brand_name = ""
    brand = getBrand(brand_name)
    search(brand)

if __name__ == "__main__":
    main() 