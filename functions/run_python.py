import os
import subprocess
def run_python_file(working_directory, file_path):
    # check if file_path is outside the working directory
    full_path_working_directory = os.path.abspath(working_directory)
    full_path_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path_file_path.startswith(full_path_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    #check if file path exists
    if os.path.isfile(full_path_file_path):
        file_name = os.path.basename(full_path_file_path)
        if file_name.endswith('.py'):
            cmd = ['python3', file_name]
            try:
                res = subprocess.run(cmd, timeout=30, capture_output=True, text=True, cwd=full_path_working_directory)
                result_parts = []
                if res.stdout:
                    result_parts.append(f"STDOUT: {res.stdout}")
                if res.stderr:
                    result_parts.append(f"STDERR: {res.stderr}")
                if res.returncode != 0:
                    result_parts.append(f"Process exited with code {res.returncode}")
                if not result_parts:
                    return "No output produced."
                else:
                    str_res = "\n".join(result_parts)
                    return str_res
            except Exception as e:
                return f"Error: executing Python file: {e}"

        else:
            return f'Error: "{file_path}" is not a Python file.'
    else:
        return f'Error: File "{file_path}" not found.'