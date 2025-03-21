import json

# Load the JSON file
with open('jina/data/brands/Levi\'s_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert the entire JSON to a string
json_string = json.dumps(data, indent=2)

# Count characters
char_count = len(json_string)

# Rough token estimation (1 token ≈ 4 characters)
estimated_tokens = int(char_count / 4)

print(f"Character count: {char_count}")
print(f"Estimated token count: {estimated_tokens}") 