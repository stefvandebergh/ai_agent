import os 

def get_files_info(working_directory, directory="."):   
    working_directory_absolute = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_absolute, directory))
    valid = os.path.commonpath([working_directory_absolute, target_dir]) == working_directory_absolute
    if not valid:
        return f'Error: cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir} is not a directory'
    
    # take a look at items inside directory, write them to directory_items
    try:
        directory_items = os.listdir(target_dir)
    except OSError as e:
        return f"Error  {e}"

    returnstring =""
    for item in directory_items:
        # get size of item
        size = 0
        try:
            size = os.path.getsize(target_dir +f"/{item}")
        except OSError as e:
            return f"Error  {e}"
        
        # get whether directory is valid
 
        valid_item = os.path.isdir(target_dir +f"/{item}")
 

        # append to returnstring
        returnstring += f"- {item}: file_size={size} bytes, is_dir={valid_item}\n"

    return returnstring