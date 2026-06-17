from tools import CODE_TOOLS, run_python,list_files, read_file, write_file,calculate_math
from dotenv import load_dotenv
import os
import json
import re
import time
import requests
import subprocess
from openai import OpenAI


CODE_SYSTEM_PROMPT = """You are a coding agent. You write, run, and debug Python code to solve tasks.

Available tools:
{tool_descriptions}

Format — to use a tool:

THOUGHT: <your reasoning>
ACTION: <tool_name>
ACTION_INPUT: {{"arg1": "value1", "arg2": "value2"}}

Format — when done:

THOUGHT: <final reasoning>
FINAL_ANSWER: <your answer>

## Rules
- ONE action per turn. Wait for OBSERVATION.
- After writing code to a file, always run_python to TEST it.
- If a test fails, read the error, fix the code, try again.
- Verify your work before giving FINAL_ANSWER.
- Include print() statements so you can see output.
"""

load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)


def run_code_agent(user_query, max_iterations=15, verbose=True):
    """ReAct agent with coding tools."""
    tool_desc = "\n".join(f"- {t['desc']}" for t in CODE_TOOLS.values())
    system = CODE_SYSTEM_PROMPT.format(tool_descriptions=tool_desc)

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_query},
    ]

    if verbose:
        print(f"\n{'='*60}")
        print(f"🧑 TASK: {user_query}")
        print(f"{'='*60}")

    for i in range(max_iterations):
        if verbose:
            print(f"\n--- Iteration {i+1}/{max_iterations} ---")

        response = client.chat.completions.create(
            model="openrouter/free", messages=messages,
            temperature=0, max_tokens=1500,
        )

        text = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": text})

        thought_match = re.search(r"THOUGHT:\s*(.+?)(?=ACTION:|FINAL_ANSWER:|$)", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else ""
        if verbose and thought:
            print(f"💭 THOUGHT: {thought[:200]}")

        if "FINAL_ANSWER:" in text:
            answer = text.split("FINAL_ANSWER:")[-1].strip()
            if verbose:
                print(f"\n{'='*60}")
                print(f"✅ DONE in {i+1} iteration(s)")
                print(f"{'='*60}")
                print(f"📝 {answer[:500]}")
            return answer

        action_match = re.search(r"ACTION:\s*(\w+)", text)
        input_match = re.search(r"ACTION_INPUT:\s*(.+?)(?:\nTHOUGHT|\nACTION|\nFINAL|$)", text, re.DOTALL)

        if not action_match:
            messages.append({"role": "user", "content": "Use ACTION + ACTION_INPUT or FINAL_ANSWER."})
            if verbose:
                print("⚠️  Format issue, nudging...")
            continue

        tool_name = action_match.group(1).strip()
        raw_input = input_match.group(1).strip() if input_match else "{}"

        if verbose:
            print(f"🔧 ACTION: {tool_name}")

        if tool_name not in CODE_TOOLS:
            observation = json.dumps({"error": f"Unknown tool '{tool_name}'. Available: {list(CODE_TOOLS.keys())}"})
        else:
            try:
                args = json.loads(raw_input)
                observation = CODE_TOOLS[tool_name]["fn"](**args)
            except json.JSONDecodeError:
                try:
                    observation = CODE_TOOLS[tool_name]["fn"](raw_input.strip("\"'"))
                except Exception as e:
                    observation = json.dumps({"error": f"Parse + fallback failed: {e}"})
            except Exception as e:
                observation = json.dumps({"error": str(e)})

        if verbose:
            obs_short = observation[:250] + "..." if len(observation) > 250 else observation
            print(f"👁️  OBSERVATION: {obs_short}")

        messages.append({"role": "user", "content": f"OBSERVATION: {observation}"})

    return "Max iterations reached."


result = run_code_agent(
    "Write a Python function called 'is_prime(n)' that checks if a number is prime. "
    "Save it to 'prime.py'. Then write a test script that imports it and tests with: "
    "1, 2, 13, 15, 97, 100. Print the results."
)