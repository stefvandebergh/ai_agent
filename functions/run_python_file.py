import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_absolute, file_path))
        valid = os.path.commonpath([working_directory_absolute, target_dir]) == working_directory_absolute
        if not valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
       
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args:
            command.extend(args)
        

        completed_process = subprocess.run(command, cwd = working_directory_absolute, text = True, timeout= 30,  capture_output= True)
        output_string = ""
        # print(completed_process.stdout)
        # print(completed_process.stderr)
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}"
        if completed_process.stderr and completed_process.stderr:
            output_string += "\nNo output produced"
        else:
            output_string += f"STDOUT: {completed_process.stdout}"
            output_string += f"STDERR: {completed_process.stderr}"


        return output_string
    
    except OSError as e:
        return f"Error: executing Python file :{e}"