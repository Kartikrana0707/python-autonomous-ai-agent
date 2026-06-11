import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    Provides a list of files, sizes, and types within a specified directory.
    Safe for LLM Agent use with strict path sandboxing.
    """
    # 1. Establish absolute baseline for the allowed workspace
    abs_working_dir = os.path.abspath(working_directory)
    
    # 2. Handle fallback for empty/None arguments gracefully
    if directory is None or directory.strip() in ("", "."):
        directory = "."
        
    # 3. Resolve the target path relative to the working directory
    # This prevents the double-folder accumulation bug
    abs_directory = os.path.abspath(os.path.join(abs_working_dir, directory))
    
    # 4. Agent Sandbox Guard: Prevent Path Traversal Exploits
    # Adds system-specific separators to prevent prefix matching exploits
    if not abs_directory.startswith(abs_working_dir + os.sep) and abs_directory != abs_working_dir:
        return f"Error: Access denied. Target '{directory}' is outside the allowed working directory."
        
    # 5. Check existence to allow the Agent to handle its own typos
    if not os.path.exists(abs_directory):
        return f"Error: The path '{directory}' does not exist inside the workspace."

    # 6. Handle File Queries: If the Agent looks up a specific file directly
    if os.path.isfile(abs_directory):
        try:
            size = os.path.getsize(abs_directory)
            filename = os.path.basename(abs_directory)
            return f"- {filename}: file_size={size} bytes, is_directory=False\n"
        except OSError as e:
            return f"Error: Could not read file statistics. {str(e)}"

    # 7. Handle Directory Queries: List contents safely
    final_response = f"Contents of directory '{directory}':\n"
    try:
        contents = os.listdir(abs_directory)
        if not contents:
            return f"The directory '{directory}' is empty."
            
        for content in contents:
            content_path = os.path.join(abs_directory, content)
            is_dir = os.path.isdir(content_path)
            
            # Catch locked/system files without breaking the whole loop
            try:
                size = os.path.getsize(content_path)
            except OSError:
                size = 0
                
            final_response += f"  - {content}: file_size={size} bytes, is_directory={is_dir}\n"
            
    except PermissionError:
        return f"Error: Permission denied. The agent does not have access to read '{directory}'."
    except Exception as e:
        return f"Error unexpected: {str(e)}"       
    return final_response

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Lists the files, sizes, and types within a specified directory. Use this tool "
        "to explore the project structure, discover what files exist, find where code is located, "
        "or check if a specific directory contains files before reading them."
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
            "directory": {
                "type": "STRING",
                "description": (
                    "The relative path of the directory to list the contents of. "
                    "Defaults to '.' or an empty string to explore the root workspace. "
                    "Example: 'src', 'tests', or '.'."
                )
            }
        },
        "required": [
            "working_directory"
        ]
    }
)

