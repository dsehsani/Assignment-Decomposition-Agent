# Assignment Decomposition Agent

This project is a simple Python CLI tool that takes an assignment PDF and a due date, then breaks the assignment into clear, manageable mini tasks paced from today through the deadline.

The goal is to reduce procrastination by turning vague assignments into concrete, time bounded action steps.

## What it does

You provide:
- An assignment PDF
- A deadline date

The script:
- Reads the assignment content
- Calculates the available time from today to the due date
- Generates a structured list of mini tasks
- Limits each task to at most 60 minutes
- Outputs strictly validated JSON using a JSON Schema
- Prints a clean, readable task plan in the terminal

## Example output

- Assignment title
- Deadline
- List of mini tasks
  - Task description
  - Estimated minutes
  - Suggested due by date

## Tech stack

- Python
- OpenAI Responses API
- JSON Schema validation
- dotenv for environment management

## Project structure
Project-Winter/
├── plan.py
├── schema.json
├── input.pdf
├── requirements.txt
└── .env

## Setup

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Create a .env file
```bash
OPENAI_API_KEY=your_api_key_here
```

3. Add your assignment PDF as input.pdf


## Run the Script
```bash
python plan.py
```

You will be prompted to enter the assignment deadline in YYYY-MM-DD format.


### Why this Exists
Assignments often feel overwhelming because they lack structure. This tool forces clarity by converting a single large task into realistic, scheduled work sessions that are easy to start and easy to track.

Future improvements
	•	Export tasks to calendar
	•	Support multiple assignments
	•	Web or desktop UI
	•	Task completion tracking


# Assignment Decomposition Agent

A lightweight Python CLI tool that takes an assignment PDF and a due date, then breaks the assignment into clear, manageable mini‑tasks automatically scheduled from today through the deadline.

The goal is to reduce procrastination by transforming vague, overwhelming assignments into concrete, time‑bounded action steps.

---

## What This Tool Does

You provide:
- An assignment PDF
- A deadline date

The tool:
- Extracts and analyzes the assignment content
- Calculates the available time between today and the deadline
- Generates a structured list of mini‑tasks
- Caps each task at a maximum of 60 minutes
- Assigns suggested “complete by” dates for each task
- Outputs strictly validated JSON using a JSON Schema
- Prints a clean, human‑readable task plan in the terminal

---

## Example Output

- Assignment title
- Deadline
- Mini‑task list
  - Task description
  - Estimated duration (minutes)
  - Suggested due‑by date

---

## Tech Stack

- Python
- OpenAI Responses API
- JSON Schema validation
- python‑dotenv for environment variable management

---

## Project Structure

```
Project-Winter/
├── plan.py
├── schema.json
├── input.pdf
├── requirements.txt
└── .env
```

---

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

3. Add your assignment PDF as `input.pdf`.

---

## Running the Tool

```bash
python plan.py
```

You will be prompted to enter the assignment deadline in `YYYY-MM-DD` format.

---

## Why This Exists

Assignments often feel overwhelming because they lack structure and clear starting points. This tool forces clarity by converting a single large task into realistic, scheduled work sessions that are easy to begin and easy to track.

---

## Future Improvements

- Export tasks to a calendar
- Support multiple assignments
- Web or desktop UI
- Task completion tracking