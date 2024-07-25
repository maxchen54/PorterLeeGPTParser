from openai import OpenAI
import os
from dotenv import load_dotenv
from argparse import ArgumentParser

load_dotenv()

# Define your API key and the endpoint URL
api_key = os.getenv('OPENAI_API_KEY')

parser = ArgumentParser(description="""\
Upload .jsonl file to OpenAI for fine-tuning.
""")
parser.add_argument('-j', '--jsonpath', required=True,
                    help='The file that holds json data to be uploaded (required)')

args = parser.parse_args()
json_merged_dataset = args.jsonpath

client = OpenAI(api_key=api_key)

file_response = client.files.create(
    file=open(json_merged_dataset, "rb"),
    purpose="fine-tune"
)

print("File ID:", file_response.id)
print(" the file data : ", file_response)
