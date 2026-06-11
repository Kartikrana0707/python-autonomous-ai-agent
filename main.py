import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time
# Import all functions and their matching schemas
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

load_dotenv()

# Define the absolute workspace boundary (current directory by default)
WORKING_DIRECTORY = os.path.abspath(os.getcwd())

# Map function names to their actual python executables
TOOL_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

# It is the agent system prompt so it understands what it is and what it needs to do
system_prompt = f"""
You are an expert autonomous AI software engineering agent. Your current working directory is safely locked at: '{WORKING_DIRECTORY}'.

You have a complete toolkit to manage code:
1. List files/directories to understand the structure (`get_files_info`).
2. Read files to understand or inspect existing logic (`get_file_content`).
3. Write/overwrite files to build features or fix bugs (`write_file`).
4. Execute Python scripts to test your work and verify outputs (`run_python_file`).

STRATEGY & WORKFLOW:
- Always check the files in the directory before assuming what exists.
- If an execution error (STDERR) occurs, read the code, fix it using `write_file`, and re-run it.
- Work iteratively until the user's objective is fully satisfied.
- Note: Always pass the absolute path '{WORKING_DIRECTORY}' as the `working_directory` parameter to all tools.
"""

# Argument parsing
if len(sys.argv) < 2:
    print("❌ Error: Please provide a prompt. Example: python main.py 'fix the bug in test.py'")
    sys.exit(1)

verbose_flag = False
if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    verbose_flag = True

user_prompt = sys.argv[1]

# Initialize Gemini Client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in environment variables.")
    sys.exit(1)
    
client = genai.Client(api_key=api_key)

# Initialize the chat history array with the user's request
messages = [
    types.Content(role="user", parts=[types.Part.from_text(text=user_prompt)]),
]

# Bundle all schemas together into Gemini's toolbelt
available_tools = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[available_tools],
    temperature=0.2, # Lower temperature makes the agent more deterministic and logical
)

print(f"🚀 Starting Agent with prompt: '{user_prompt}'\n" + "="*50)

# The Agent Execution Loop (Handles dynamic Multi-Turn Tool Calls)
max_iterations = 15  # Prevents infinite loops if the agent gets stuck
for iteration in range(max_iterations):
    if iteration > 0:
        print("⏳ Rate limit safeguard: Pausing for 12 seconds...")
        time.sleep(12)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=config,
    )
    
    if response is None:
        print("❌ Error: Received a malformed response from Gemini.")
        break
        
    # If the model has text to output, append it to the chat history and display it
    if response.text:
        print(f"\n🤖 Agent:\n{response.text}")
        messages.append(types.Content(role="model", parts=[types.Part.from_text(text=response.text)]))
        
    # Check if the model wants to call one or more functions
    if response.function_calls:
        # Save the model's intent to call a function into history
        messages.append(types.Content(role="model", parts=response.candidates[0].content.parts))
        
        # Container to hold responses for this round of function executions
        function_responses = []
        
        for function_call in response.function_calls:
            func_name = function_call.name
            func_args = function_call.args
            
            if verbose_flag:
                print(f"\n[VERBOSE] Agent requested function: {func_name} with args: {dict(func_args)}")
            else:
                print(f"⚙️ Running tool: {func_name}...")
                
            # Execute the matching tool safely
            if func_name in TOOL_MAP:
                try:
                    # Execute the Python function using kwargs unpacked from Gemini's call
                    tool_output = TOOL_MAP[func_name](**func_args)
                except Exception as e:
                    tool_output = f"Execution Error: Failed to execute tool locally. Details: {str(e)}"
            else:
                tool_output = f"Error: Tool '{func_name}' is not registered in the system."
                
            if verbose_flag:
                print(f"[VERBOSE] Tool Output:\n{tool_output}")
                
            # Pack the output into the format Gemini expects for a Function Response
            function_responses.append(
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": tool_output}
                )
            )
            
        # Send the execution results back to the conversation thread
        messages.append(types.Content(role="user", parts=function_responses))
        
        # Keep the loop moving forward to let Gemini analyze the tool's result
        continue
    else:
        # No more function calls requested by the model! The agent has finished its job.
        print("\n" + "="*50 + "\n✅ Mission Completed Successfully.")
        break
else:
    print("\n⚠️ Agent stopped automatically: Reached safety maximum execution limit.")