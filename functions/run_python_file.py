import subprocess
import os
import sys
def run_python_file(working_directory,file_path):
    abs_working_dir=os.path.abspath(working_directory)
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} path is outside the working directory"
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"
    if not file_path.endswith(".py"):
        return f"Error: {file_path} is not a python file"
    try:
        result=subprocess.run([sys.executable, abs_file_path],cwd=abs_working_dir, timeout=30,capture_output=True,text=True)
        final_output= f"""
        Ran {file_path}\n
        Return Code: {result.returncode}\n
        STDOUT:\n
        {result.stdout}\n
        STDERR:\n
        {result.stderr}\n
        """
        if result.returncode != 0:
            return f"Error: {file_path} failed to run Output: {result.stderr}"
        if result.stdout == "" and result.stderr == "":
            return "No output"
        return final_output
    except Exception as e:
        return f"Error: {file_path} failed to run {str(e)}"

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a specified Python (.py) file within the workspace and captures its output. "
        "Use this tool to run code, execute scripts, execute tests, or verify if a bug fix works. "
        "Note: Execution will automatically timeout if it takes longer than 30 seconds."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "working_directory": {
                "type": "STRING",
                "description": (
                    "The absolute path to the root directory of the allowed workspace. "
                    "Always look up or maintain the active project root directory for this."
                )
            },
            "file_path": {
                "type": "STRING",
                "description": (
                    "The relative path of the Python file to execute, relative to the working_directory. "
                    "Must end with '.py'. Example: 'main.py' or 'scripts/process_data.py'."
                )
            }
        },
        "required": [
            "working_directory",
            "file_path"
        ]
    }
)