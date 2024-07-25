from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()
#file_id = 'file-HdL21xbApvrKq7zwUF7FfZhp'   # wrong
#file_id = 'file-4AqxGRr7TtBBiZe7edULvtC0'    # wrong
#file_id = 'file-uVYre5TKHLrnws5UmoDSauU2'   ## 4 files
#file_id = 'file-uSUxCmz8hggSIX4Basaf39Ux'   # 1 file
#file_id = 'file-ECZIlzExzZRjSqy3uVBvaKjp'    # 1 pair format file
api_key = os.getenv('OPENAI_API_KEY')
file_id = os.getenv('FILE_ID')   #  1 file 4_
validation_id = os.getenv('VALIDATION_ID')
my_job_id = os.getenv('JOB_ID')

fine_tune_model = 'gpt-3.5-turbo-0125'
#fine_tune_model = 'davinci-002'
client = OpenAI(api_key=api_key)

fine_tune_response = client.fine_tuning.jobs.create(
    training_file=file_id,
    validation_file=validation_id,
    model=fine_tune_model
)

job_id = fine_tune_response.id
print("Fine tune job ID:", job_id)
print(" the fine tune : ", fine_tune_response)

# Retrieve the state of a fine-tune and wait for it to complete
status = client.fine_tuning.jobs.retrieve(job_id).status
if status not in ["succeeded", "failed"]:
    print(f"Job not in terminal status: {status}. Waiting.")
    while status not in ["succeeded", "failed"]:
        time.sleep(60)
        status = client.fine_tuning.jobs.retrieve(job_id).status
        print(f"Status: {status}")
else:
    print(f"Finetune job {job_id} finished with status: {status}")
    print("")
print("The file tune job ", client.fine_tuning.jobs.retrieve(job_id))
fine_tune_model = client.fine_tuning.jobs.retrieve(job_id).fine_tuned_model
print("The fine tune model is : ", fine_tune_model)
