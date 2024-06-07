import subprocess
import re
import io
import contextlib

from website import make_site

import re
import subprocess
import io
import contextlib



def process(input_string):

    terminal_pattern = r'```terminal\s(.*?)```'
    python_pattern = r'```python\s(.*?)```'
    generic_code_pattern = r'```(.*?)```'



    terminal_commands = re.findall(terminal_pattern, input_string, re.DOTALL)
    for command in terminal_commands:
        subprocess.run(command.strip(), shell=True)

    python_commands = re.findall(python_pattern, input_string, re.DOTALL)
    generic_code_blocks = re.findall(generic_code_pattern, input_string, re.DOTALL)

    combined_output = ""
    for command in python_commands + generic_code_blocks:
        stdout = io.StringIO()
        stderr = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(command.strip())
        except Exception as e:
            stderr.write(str(e))

        output = stdout.getvalue().strip()
        errors = stderr.getvalue().strip()

        if output:
            combined_output += f"Output: {output}\n"
        if errors:
            if combined_output:
                combined_output += ", "
            combined_output += f"Errors: {errors}\n"

    input_string = re.sub(terminal_pattern, lambda match: '', input_string, flags=re.DOTALL)
    input_string = re.sub(python_pattern, lambda match: '', input_string, flags=re.DOTALL)
    input_string = re.sub(generic_code_pattern, lambda match: '', input_string, flags=re.DOTALL)

    return input_string.strip(), combined_output if combined_output else None

def execute_functions(function_names, input_string):
    for func_name in function_names:
        pattern = fr"\b{func_name}\(([^)]+)\)"
        matches = re.findall(pattern, input_string)
        for match in matches:
            globals()[func_name](match)
            input_string = re.sub(pattern, "", input_string, count=1)
    return input_string