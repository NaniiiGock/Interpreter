from .music import turn_music
from .datetime_mac import tell_current_datetime
from .apps_mac import open_app
from .make_call import call_by_phone_number, call_by_name
from .scheduler import schedule_command, remove_scheduled_command
from .run_generated_scripts import run_applescript, run_shell_script, run_python_script, run_scripts
import json
import re


available_functions = {
    "turn_music": turn_music,
    "tell_current_datetime": tell_current_datetime,
    "open_app": open_app,
    "call_by_phone_number": call_by_phone_number,
    "call_by_name": call_by_name,
    "schedule_command": schedule_command,
    "remove_scheduled_command": remove_scheduled_command,
    "run_scripts": run_scripts
}


def get_funcs_responses(tool_calls):
    responses = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(**function_args)
        responses.append(function_response)
    return responses


def parse_markdown_code_blocks(markdown_text):
    code_block_regex = re.compile(r'```(.*?)\\[rnt]*([\s\S]+?)```', re.MULTILINE)
    code_blocks = []

    matches = code_block_regex.finditer(markdown_text)

    for match in matches:
        language_name = match.group(1).strip().lower()  # Convert to lowercase

        # Exclude code blocks with language names containing "example"
        if 'example' not in language_name:
            code_block_content = match.group(2)

            # Replace triple backticks within a string inside the code
            code_block_with_triple_backticks_fixed = code_block_content.replace('```', '``\`')

            # Append the processed code block
            formatted_code_block = f"```{language_name}\n{code_block_with_triple_backticks_fixed}" if language_name else code_block_with_triple_backticks_fixed
            code_blocks.append(formatted_code_block)

    # Join the code blocks with two newlines
    code_block_string = '\n\n'.join(code_blocks)
    return code_block_string
