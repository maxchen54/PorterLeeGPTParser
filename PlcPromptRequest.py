from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)


default_model = 'gpt-3.5-turbo-0125'
#fine_tune_model = 'ft:gpt-3.5-turbo-0125:porter-lee-corporation::9lpGFGcW'   # 4 files
#fine_tune_model = 'ft:gpt-3.5-turbo-0125:porter-lee-corporation::9lq7lZ4t'    # 1 file
fine_tune_model = 'ft:davinci-002:porter-lee-corporation::9lqST71G'    # 1 file

completion = client.completions.create(
    model=fine_tune_model,
    prompt="Describe how Porter Lee's product utilizes externally licensed programs.",
    max_tokens=200,  # Adjust the number of tokens as needed
    temperature=0.1
)

print(str(len(completion.choices)) + " answer.")
print(completion.choices[0].text.strip())