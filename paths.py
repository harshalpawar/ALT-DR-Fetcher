import os

# Absolute path to project root
PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))
JINA_DIR = os.path.join(PROJECT_HOME, "jina")
BRANDS_DIR = os.path.join(JINA_DIR, "data", "brands")
ENV_FILE = os.path.join(PROJECT_HOME, ".env")
BRAND_LIST_FILE = os.path.join(JINA_DIR, "data", "brand_list.json")

