import atexit
import logging
import os

import readline

import llm_model.OpenAILLM.setup_llm as setup_llm
from REPL import REQUESTS_HISTORY_PATH
from REPL.functional.functional_utils import get_funcs_responses


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
    os.system("sh ../utils/logo.sh")
    while True:
        line = input("> ").strip()
        # line = "write an email to my professor at professor@email.com to as him about summer mentorship"
        if line == "exit":
            break
        llm_response = setup_llm.get_llm_response(line)
        if hasattr(llm_response, 'tool_calls'):
            tool_calls = llm_response.tool_calls
            if tool_calls:
                responses = get_funcs_responses(tool_calls)
                # do something with responses
                continue
        print(llm_response.content)



if __name__ == "__main__":
    run_repl()
