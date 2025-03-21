import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time
from tqdm import tqdm
from dotenv import load_dotenv
from paths import *
from jinaSearch import search
from jinaFormat import getFormattedWebpage
from geminiFormat import getResponse

# Load environment variables
load_dotenv(ENV_FILE)

def process_brand(brand):
    print(f"\n{'='*50}")
    print(f"Processing {brand['name']}")
    print(f"{'='*50}\n")
    
    try:
        search(brand)
        time.sleep(5) 
        getFormattedWebpage(brand)
        getResponse(brand)
        print(f"\n✅ Successfully processed {brand['name']}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error processing {brand['name']}: {e}")
        return False

def main():    
    # Load brand list
    with open(BRAND_LIST_FILE, 'r') as f:
        brands = json.load(f)['brands']

    # Process each brand
    successful = 0
    failed = 0
    
    for brand in tqdm(brands[2:], desc="Processing brands"):
        print(f"\nProcessing brand {brands.index(brand) + 1}/{len(brands)}")
        if process_brand(brand):
            successful += 1
        else:
            failed += 1
        time.sleep(5)  # Delay between brands to avoid rate limiting
    
    # Print summary
    print("\n" + "="*50)
    print("Processing Complete!")
    print(f"Total brands: {len(brands)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("="*50)

if __name__ == "__main__":
    main() 