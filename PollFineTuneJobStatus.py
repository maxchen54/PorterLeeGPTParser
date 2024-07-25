from openai import OpenAI
import time
import os
from dotenv import load_dotenv
from argparse import ArgumentParser

load_dotenv()

# Define your API key and the endpoint URL
api_key = os.getenv('OPENAI_API_KEY')

parser = ArgumentParser(description="""\
Enter your fine-tuning job ID to check its status.
""")
parser.add_argument('-j', '--jobid', required=True,
                    help='The fine-tuning job id (required)')

args = parser.parse_args()
job_id = args.jobid

client = OpenAI(api_key=api_key)

print("Fine tune job ID:", job_id)

# Retrieve the state of a fine-tune and wait for it to complete
job = client.fine_tuning.jobs.retrieve(job_id)
print("Fine tune job : ", job)

if job.status not in ["succeeded", "failed"]:
    print(f"Job not in terminal status: {job.status}. Waiting.")
    while job.status not in ["succeeded", "failed"]:
        time.sleep(60)
        job = client.fine_tuning.jobs.retrieve(job_id)
        print(f"Status: {job.status}")
else:
    print(f"Finetune job {job_id} finished with status: {job.status}")
    print("")
print("The fine tune job : ", job)
fine_tune_model = job.fine_tuned_model
print("The fine tune model is : ", fine_tune_model)
