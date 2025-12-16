from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import time 

# load enviornment 
load_dotenv()

with open("schema.json") as f:
    schema = json.load(f)

# grab API Key
if "OPENAI_API_KEY" not in os.environ:
    raise RuntimeError("OPENAI_API_KEY Missing")

# initalize client 
client = OpenAI()

# read assignment pdf 
try:
    assignment_file = client.files.create(
        file=open("input.pdf", "rb"),
        purpose="user_data"
    )

except Exception as e:
    raise RuntimeError("Failure Opening Assignment")

# Grab Deadline
deadline = input("Enter deadline for assignment (YYYY-MM-DD): ").strip()

# grab current time
current_date = time.strftime("%Y-%m-%d")

if not deadline:
    raise ValueError("Deadline cannot be empty")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            # what the system must behave as
            "role" : "system",
            "content" : "You are an assignment decomposition agent."
        },
        {
            # the task to accomplish/respond to 
            "role": "user",
            "content" : [
                {
                    "type": "input_text",
                    "text" : f"""
                        Break this assignment into clear, actionable mini-tasks.
                        Use the provided deadline to pace the work.
                        Return ONLY valid JSON that matches the schema.

                        The duration of assignment is from: Today: {current_date} to Deadline: {deadline}. Limit task to only 60 minutes a piece max.
                    """
                },
                {
                    "type": "input_file",
                    "file_id": assignment_file.id
                }
            ]
        }
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "assignment_breakdown",
            "schema": schema, 
            "strict": True
        }
    }
)

# parse output 
data = json.loads(response.output_text)

print(f"Assignment: {data['assignment_title']}")
print(f"Deadline: {data['deadline']}\n")

for task in data['mini_tasks']:
    print(f"{task['task']}")
    print("-" * len(task["task"]))
    print(f"    Estimated Time: {task['estimated_minutes']} minutes")
    print(f"    Due by: {task['due_by']}\n")

