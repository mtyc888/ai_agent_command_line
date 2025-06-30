import os
MAX_CHARS = 10000
def get_file_content(working_directory, file_path):
    full_path_working_directory = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    full_path_file_path = os.path.abspath(full_path)

    if full_path_file_path.startswith(full_path_working_directory):
        if os.path.isfile(full_path_file_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        try:
            with open(full_path_file_path,'r') as file:
                file_content_string = file.read(MAX_CHARS)
            size_content = os.path.getsize(full_path_file_path)
            if size_content > MAX_CHARS:
                file_content_string = file_content_string + f"[...File '{file_path}' truncated at 10000 characters]"
            
            return file_content_string

        except Exception as e:
            return f"Error: {e}"
    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
