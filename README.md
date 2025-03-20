# Fashion Brand Policy Retriever

## Overview
This Python script retrieves delivery and return policies for fashion brands using the Perplexity AI API. It's designed to extract structured information about a brand's shipping and return policies in India.

## Features
- Fetch detailed return and delivery policy information
- Structured response format
- Logging of API calls and responses
- Easily configurable for different brands

## Prerequisites
- Python 3.8+
- Perplexity API Key

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <project-directory>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with your Perplexity API key:
```
PERPLEXITY_API_KEY=your_api_key_here
```

## Usage

Modify the `brand` dictionary in `makeRequest.py` to change the target brand:
```python
brand = {
    "name": "H&M",
    "url": "https://www2.hm.com/en_in/index.html"
}
```

Run the script:
```bash
python makeRequest.py
```

## Output
- Generates `api_response_log.txt` with detailed API call information
- Prints response details to console

## Customization
- Adjust `system_prompt` and `user_prompt` to modify query behavior
- Modify `settings` dictionary to fine-tune API request parameters

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
[Your License Here]

## Disclaimer
This tool is for informational purposes. Always verify policies directly with the brand. 