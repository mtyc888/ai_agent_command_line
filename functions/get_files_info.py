import os
"""
    This function accepts a directory path and return string that represents the contents of that directory
"""
def get_files_info(working_directory, directory = None):
    full_path_working_directory = os.path.abspath(working_directory)
    full_path_directory = os.path.abspath(directory)

    if(os.path.isdir(directory) == False):
        return f'Error: "{directory}" is not a directory'
    
    if(full_path_directory.startswith(full_path_working_directory)):
        try:
            content_string = ""
            items = os.listdir(full_path_directory)
            list_of_full_content = []
            for item in items:
                full_path_item = os.path.join(full_path_directory, item)
                file_size = os.path.getsize(full_path_item)
                is_dir = os.path.isdir(full_path_item)
                full_str = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
                list_of_full_content.append(full_str)
            
            content_string = "\n".join(list_of_full_content)
            
            return content_string

        except Exception as err:
            return f"Error: {err}"
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'