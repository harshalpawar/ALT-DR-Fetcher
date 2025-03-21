import os
import json
import sys
import time
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def check_venv():
    """Check if script is running in a virtual environment"""
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("❌ Error: Not running in a virtual environment")
        print("Please activate your venv before running this script")
        sys.exit(1)

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['JINA_API_KEY', 'GEMINI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        sys.exit(1)

def process_brand(brand_name):
    print(f"\n{'='*50}")
    print(f"Processing {brand_name}")
    print(f"{'='*50}\n")
    
    try:
        # Step 1: Run jinaSearch.py
        print(f"🔍 Step 1: Running jinaSearch for {brand_name}")
        result = os.system(f'python jinaSearch.py "{brand_name}"')
        if result != 0:
            raise Exception("jinaSearch.py failed")
        time.sleep(2)  # Small delay between steps
        
        # Step 2: Run jinaFormat.py
        print(f"\n📝 Step 2: Running jinaFormat for {brand_name}")
        result = os.system(f'python jinaFormat.py "{brand_name}"')
        if result != 0:
            raise Exception("jinaFormat.py failed")
        time.sleep(2)  # Small delay between steps
        
        # Step 3: Run geminiFormat.py
        print(f"\n🤖 Step 3: Running geminiFormat for {brand_name}")
        result = os.system(f'python geminiFormat.py "{brand_name}"')
        if result != 0:
            raise Exception("geminiFormat.py failed")
        
        print(f"\n✅ Successfully processed {brand_name}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error processing {brand_name}: {e}")
        return False

def main():
    # Check environment variables
    check_venv()
    check_environment()
    
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    brands_dir = os.path.join(data_dir, 'brands')
    os.makedirs(brands_dir, exist_ok=True)
    
    # Check if brand_list.json exists
    brand_list_path = os.path.join(data_dir, 'brand_list.json')
    if not os.path.exists(brand_list_path):
        print(f"❌ Error: {brand_list_path} not found")
        sys.exit(1)
    
    # Load brand list
    try:
        with open(brand_list_path, 'r') as f:
            brands = json.load(f)['brands']
    except Exception as e:
        print(f"❌ Error loading brand_list.json: {e}")
        sys.exit(1)
    
    # Process each brand
    successful = 0
    failed = 0
    
    for brand in tqdm(brands, desc="Processing brands"):
        print(f"\nProcessing brand {brands.index(brand) + 1}/{len(brands)}")
        if process_brand(brand['name']):
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