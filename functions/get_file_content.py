import os 
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets content from a file in a specified file path relative to the working directory, providing one string that is truncated if it gets longer than 10 000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to retrieve file conten from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_absolute, file_path))
        valid = os.path.commonpath([working_directory_absolute, target_dir]) == working_directory_absolute
        if not valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        content = ""
        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except OSError as e:
        return f"Error :{e}"