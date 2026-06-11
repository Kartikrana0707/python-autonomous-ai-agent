from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
def main():
    working_dir="calculator"
    """print(get_files_info(working_dir))
    print(get_files_info(working_dir, "functions"))
    print(get_file_content(working_dir,"main.py"))"""
    print(run_python_file(working_dir,"tests.py"))
    print(run_python_file(working_dir,"../main.py"))
    print(run_python_file(working_dir,"nonexistent.py"))


main()