import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": (
            "Run a Python file and return its output. This is the only tool to choose when "
            "the user asks to run, execute, or test a specific Python file. Call it directly "
            "with the path from the user. Never call get_files_info or get_file_content first: "
            "this tool already checks whether the file exists and returns an error if needed."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the Python file",
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path[len(file_path) - 3 :] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]

        if args:
            command.extend(args)

        process = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )

        output = ""

        if process.returncode != 0:
            output += f"Process exited with code {process.returncode}\n"

        if process.stdout:
            output += f"STDOUT:\n{process.stdout}"

        if process.stderr:
            output += f"STDERR:\n{process.stderr}"

        if not process.stdout and not process.stderr:
            output += "No output produced"

        return output
    except Exception as e:
        return f"Error: {e}"
