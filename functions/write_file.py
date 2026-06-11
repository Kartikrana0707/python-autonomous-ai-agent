import os
def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # 1. Security Check (Directory Traversal Protection)
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} path is outside the working directory"
    
    # 2. Prevent overwriting a folder by accident
    if os.path.isdir(abs_file_path):
        return f"Error: {file_path} is a directory, cannot write file content to it"

    # 3. Dynamic Directory Creation
    parent_dir = os.path.dirname(abs_file_path)
    try:
        # This is safe to run even if the directory already exists
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        return f"Error creating directory structure: {str(e)}"
        
    # 4. Write File Content
    try:
        with open(abs_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully written to {file_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes the specified string content to a file. Use this tool to create new files, "
        "overwrite existing code/text files, or generate logs/configs. "
        "It automatically creates any missing parent directories required by the file path."
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
                    "The relative path of the file to write, relative to the working_directory. "
                    "Example: 'src/utils.py' or 'config.json'."
                )
            },
            "content": {
                "type": "STRING",
                "description": (
                    "The exact, full text or code content to be written into the file."
                )
            }
        },
        "required": [
            "working_directory",
            "file_path",
            "content"
        ]
    }
)
