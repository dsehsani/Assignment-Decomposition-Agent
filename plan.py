from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
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

# grab current time
tz = ZoneInfo("America/Los_Angeles")
current_date = datetime.now(tz).strftime("%Y-%m-%d")

if not deadline:
    raise ValueError("Deadline cannot be empty")

if deadline < current_date:
    raise ValueError("Deadline already passed")

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
                            You are an assignment decomposition agent.

                            Goal:
                            Create a realistic, non-overwhelming plan from TODAY to DEADLINE using the assignment PDF as the single source of truth.
                            The plan should help a stressed student feel confident starting immediately.

                            Planning principles:
                            - Avoid vague or administrative filler tasks unless strictly necessary.
                            - Break work into steps that reduce cognitive load, not just milestones.
                            - Prefer concrete “how-to” steps over generic labels like “implement” when a task is large.
                            - Each task should have a clear definition of done.

                            Task design rules:
                            - Each mini_task must take <= 60 minutes.
                            - If a task would realistically take longer, split it into smaller steps.
                            - Use actionable verbs and include what will be produced (file, output, verification).
                            - Do not include redundant setup tasks unless the PDF explicitly requires external files or downloads.
                            - Time estimates should be realistic for a prepared student, not worst-case.
                            - Packaging / submission tasks should be short unless complexity is justified.

                            Scheduling rules:
                            - Tasks must be ordered in the sequence they should be done.
                            - due_by must be YYYY-MM-DD, non-decreasing, and <= DEADLINE.
                            - Distribute tasks evenly across days; avoid overloading a single day.
                            - Include buffers near the end for testing and review.

                            Required structure:
                            - Include requirements extraction or clarification ONLY if needed.
                            - Include planning steps that reduce overwhelm (e.g. pseudocode, outlining).
                            - Include implementation, verification, and final review.
                            - If something is extra credit, clearly label it as optional.

                            Hard constraints:
                            - Return ONLY valid JSON matching the provided schema (strict).
                            - Use only information present in the PDF.
                            - Do not invent requirements, filenames, or grading criteria.

                            Context:
                            Today: {current_date}
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

# safely extract model output text
raw_output = response.output_text

if isinstance(raw_output, list):
    raw_output = "".join(raw_output)

if not isinstance(raw_output, str):
    raise RuntimeError("Unexpected response.output_text format")

# parse JSON with debug help
try:
    data = json.loads(raw_output)

except json.JSONDecodeError as e:
    print("Failed to parse JSON from model output")
    print("Raw output preview:")
    print(raw_output[:500])
    raise e

# basic schema sanity checks
required_top_keys = ["assignment_title", "deadline", "mini_tasks"]
for key in required_top_keys:
    if key not in data:
        raise KeyError(f"Missing required key in response: {key}")

if not isinstance(data["mini_tasks"], list):
    raise TypeError("mini_tasks must be a list")

print(f"Assignment: {data['assignment_title']}")
print(f"Deadline: {data['deadline']}\n")

for task in data['mini_tasks']:
    required_task_keys = ["task", "estimated_minutes", "due_by"]
    for k in required_task_keys:
        if k not in task:
            raise KeyError(f"Missing task field: {k}")
    print(f"{task['task']}")
    print("-" * len(task["task"]))
    print(f"    Estimated Time: {task['estimated_minutes']} minutes")
    print(f"    Due by: {task['due_by']}\n")
