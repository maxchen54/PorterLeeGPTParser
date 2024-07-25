import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Define your API key and the endpoint URL
api_key = os.getenv('OPENAI_API_KEY')
url = 'https://api.openai.com/v1/chat/completions'
default_model = 'gpt-3.5-turbo-0125'
#fine_tune_model = 'ft:gpt-3.5-turbo-0125:porter-lee-corporation::9lpGFGcW'   # 4 files
fine_tune_model = 'ft:gpt-3.5-turbo-0125:porter-lee-corporation::9lq7lZ4t'    # 1 file
#fine_tune_model = 'ft:davinci-002:porter-lee-corporation::9lqST71G'    # 1 file

# Define the headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# Define the data for the request
data = {
    'model': fine_tune_model,  # You can change this to 'gpt-3.5-turbo' for GPT-3.5
    'messages': [
        {'role': 'system', 'content': 'Provide response for a Request For Proposal.'},
        {'role': 'user', 'content': 'How your product is licensed?'}
    ],
    'max_tokens': 50,
    'temperature': 0.7
}

# Send the request
response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    response_data = response.json()
    # Extract the message content from the response
    message_content = response_data['choices'][0]['message']['content']
    print('Response:', message_content)
else:
    print('Request failed with status code:', response.status_code)
    print('Response:', response.text)