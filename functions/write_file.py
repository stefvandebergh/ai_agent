import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content into the file pointed to by the file_path. ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type= types.Type.STRING,
                description= "The content which will be written into the file at the given file path."
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_absolute, file_path))
        valid = os.path.commonpath([working_directory_absolute, target_dir]) == working_directory_absolute
        if not valid:
            return f'Error: cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir), exist_ok = True)
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except OSError as e:
        return f"Error :{e}"
    

    