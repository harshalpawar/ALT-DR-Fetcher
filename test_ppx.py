import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Initialize Perplexity API Client
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# Define a test query
messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant that provides clear and concise answers."
    },
    {
        "role": "user",
        "content": "What is H&M's return and delivery policy?"
    },
]

# Make API call (Non-streaming response)
response = client.chat.completions.create(
    model="sonar-pro",  # Perplexity's model
    messages=messages
)

# Print response
print("✅ API Call Successful!\n")
print("🔍 Response:\n", response.choices[0].message.content)
