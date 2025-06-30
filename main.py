import os
from google import genai
from dotenv import load_dotenv
import sys


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main(prompt):

    if len(prompt) == 1:
        sys.exit(1)
    load_dotenv()
    # this basically tells the llm how to use the functions
    schema_get_files_info = genai.types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "directory": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    schema_get_file_content = genai.types.FunctionDeclaration(
        name="get_file_content",
        description="Get the contents of a file, contrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="This is the file path to the file you want to get content from.",
                ),
            },
        ),
    )
    schema_write_file = genai.types.FunctionDeclaration(
        name="write_file",
        description="Get the contents of a file, contrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="Overwrites or creates a file with new content, within the working directory.",
                ),
                "content": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="Executes a Python file within the working directory, possibly with supplied arguments."
                )
            },
        ),
    )
    schema_run_python = genai.types.FunctionDeclaration(
        name="run_python_file",
        description="Get the contents of a file, contrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="This is the file path to the python file you want to execute.",
                ),
            },
        ),
    )
    # create a list of available functions
    available_functions = genai.types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python
        ]
    )
    # gemini api call
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt[1],
        # we pass our tools to the LLM here
        config=genai.types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    if '-v' in sys.argv or '--verbose' in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    
    if response.function_calls:
        function_list = response.function_calls
        for function in function_list:
            function_name = function.name
            function_args = function.args
            print(f"Calling function: {function_name}({function_args})")
    else:
        print(response.text)



if __name__ == "__main__":
    main(sys.argv)


