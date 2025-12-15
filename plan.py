from openai import OpenAI
from dotenv import load_dotenv
import json
import os

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

if not deadline:
    raise ValueError("Deadline cannot be empty")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role" : "system",
            "content" : "You are an assignment decomposition agent."
        },
        {
            "role": "user",
            "content" : [
                {
                    "type": "input_text",
                    "text" : f"""
                        Break this assignment into clear, actionable mini-tasks.
                        Use the provided deadline to pace the work.
                        Return ONLY valid JSON that matches the schema.

                        Deadline: {deadline}
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

# print ouput
print(response.output_text)







