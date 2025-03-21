import json
from paths import BRAND_LIST_FILE

def getBrand(brand_name):
    # Load brand dictionary from JSON file
    with open(BRAND_LIST_FILE, 'r') as f:
        brand_dict = json.load(f)['brands']

    brand = next((b for b in brand_dict if b["name"] == brand_name), None)
    return brand