import atexit
import logging
import os
import json

import readline

import llm_model.OpenAILLM.setup_llm as setup_llm
from REPL import REQUESTS_HISTORY_PATH
from REPL.functional.music import turn_music


def save_history():
    """Save the readline history to a file."""
    readline.write_history_file(REQUESTS_HISTORY_PATH)


atexit.register(save_history)


def read_history():
    if readline.get_current_history_length() == 0:
        try:
            readline.read_history_file(REQUESTS_HISTORY_PATH)
        except PermissionError as pe:
            logging.error(f"Permission denied for history file: {REQUESTS_HISTORY_PATH}. Error: {pe}")
        except FileNotFoundError:
            logging.warning(f"History file not found: {REQUESTS_HISTORY_PATH}")


def run_repl():
    """Run the REPL (Read-Eval-Print Loop)."""
    read_history()
    os.system("sh utils/logo.sh")
    while True:
        line = input("> ").strip()
        # line = "Play song You Drive My Four Wheel Coffin"
        if line == "exit":
            break
        llm_response = setup_llm.generate_code_with_litellm(line)
        tool_calls = llm_response.tool_calls

        if tool_calls:
            available_functions = {
                "turn_music": turn_music,
            }
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
        # break


if __name__ == "__main__":
    run_repl()
