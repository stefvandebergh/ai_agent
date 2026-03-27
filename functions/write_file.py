import os

def write_file(working_dir, file_path, content):
    try:
        working_directory_absolute = os.path.abspath(working_dir)
        target_dir = os.path.normpath(os.path.join(working_directory_absolute, file_path))
        valid = os.path.commonpath([working_directory_absolute, target_dir]) == working_directory_absolute
        if not valid:
            return f'Error: cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir, exist_ok = True))
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except OSError as e:
        return f"Error :{e}"
    

    