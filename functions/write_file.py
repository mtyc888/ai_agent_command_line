import os

def write_file(working_directory, file_path, content):
    full_path_working_directory = os.path.abspath(working_directory)
    full_path_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if full_path_file_path.startswith(full_path_working_directory):
        try:
            # get the parent directories
            parent_directories = os.path.dirname(full_path_file_path)
            if os.path.exists(parent_directories) == False:
                os.makedirs(parent_directories)
            with open(full_path_file_path, "w") as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
    else:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'