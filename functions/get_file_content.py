import os
MAX_CHARS=10000
def get_file_content(working_directory:str, file_path):
    abs_working_dir=os.path.abspath(working_directory)
    abs_file_path=os.path.abspath(os.path.join(working_directory,file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path}path is outside the working directory"
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"

    file_content_string=""
    try:
        with open(abs_file_path,'r',encoding='utf-8')as f:
            file_content_string=f.read(MAX_CHARS)
            if len(file_content_string)>=MAX_CHARS:
                file_content_string+="\n...[TRUNCATED]" 
        return file_content_string
    except Exception as e:
        return f"Error reading file: {str(e)}"

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads and retrieves the text content of a specific file. Use this tool "
        "whenever you need to examine, analyze, debug, or read the code/text inside a file. "
        "Outputs up to 10,000 characters and truncates if the file is larger."
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
                    "The relative path of the file to be read, relative to the working_directory. "
                    "Example: 'src/main.py' or 'README.md'."
                )
            }
        },
        "required": [
            "working_directory",
            "file_path"
        ]
    }
)  
        