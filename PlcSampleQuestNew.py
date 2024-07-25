from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Define your API key and the endpoint URL
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

default_model = 'gpt-3.5-turbo-0125'
fine_tune_model = 'ft:gpt-3.5-turbo-0125:porter-lee-corporation::9lpGFGcW'   # 4 files
#fine_tune_model = 'ft:gpt-3.5-turbo-0125:porter-lee-corporation::9lq7lZ4t'    # 1 file
#fine_tune_model = 'ft:gpt-3.5-turbo-0125:porter-lee-corporation::9lsfEVf6'    # 1 file C_
completion = client.chat.completions.create(
    model=fine_tune_model,
    temperature=0.1,
    messages=[
        {"role": "user", "content": "What is a minimum setup for on premises, include an overview of architecture."}
    ]

)

print(str(len(completion.choices)) + " answer.")
print(completion.choices[0].message.content)