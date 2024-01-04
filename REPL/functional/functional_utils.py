from .music import turn_music
from .datetime_mac import tell_current_datetime
from .apps_mac import open_app
from .make_call import call_by_phone_number, call_by_name
from .scheduler import schedule_command, remove_scheduled_command
from .email_writer import compose_email
from .write_message import message_by_phone_number, message_by_contact_name
from .noter import make_note
from .voice_over import tell_number_unread_messages
from .run_generated_scripts import run_scripts, check_language
from .safari_surfer import search_google
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
    "run_scripts": run_scripts,
    "compose_email": compose_email,
    "message_by_phone_number": message_by_phone_number,
    "message_by_contact_name": message_by_contact_name,
    "make_note": make_note,
    "tell_number_unread_messages": tell_number_unread_messages,
    "search_google": search_google,
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


def get_other_response(response):
    response = response['model_extra']['content']
    code_blocks = parse_markdown_code_blocks(response)
    if not code_blocks:
        return response
    if check_language(code_blocks[0][0]):
        return run_scripts(code_blocks[0][0], code_blocks[0][1])
    return response


def parse_markdown_code_blocks(markdown_text):
    code_block_regex = re.compile(r'```(python|bash|shell|applescript)\s*([\s\S]+?)```', re.MULTILINE)
    code_blocks = []
    matches = code_block_regex.finditer(markdown_text)
    for match in matches:
        language_name = match.group(1).strip().lower()  # Convert to lowercase
        code_block_content = match.group(2)

        # Replace triple backticks within a string inside the code
        code_block_with_triple_backticks_fixed = code_block_content.replace('```', '``\`')

        # Append the processed code block
        if language_name:
            code_blocks.append(tuple([language_name, code_block_with_triple_backticks_fixed]))

    return code_blocks
