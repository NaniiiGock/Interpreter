import atexit
import logging
import os
import sys

import readline

import llm_model.OpenAILLM.setup_llm as setup_llm
from REPL import REQUESTS_HISTORY_PATH
from functional.functional_utils import pipeline_responses_processing


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


def print_error(message):
    red_text = "\033[91m"
    reset_color = "\033[0m"
    sys.stderr.write(f"{red_text}{message}{reset_color}\n")


def run_repl():
    """Run the REPL (Read-Eval-Print Loop)."""
    read_history()
    os.system("sh ../utils/logo.sh")
    while True:
        line = input("> ").strip()
        if line == "exit":
            break
        llm_response = setup_llm.get_llm_response(line)

        list_responses = pipeline_responses_processing(llm_response)

        for stout, stderr in list_responses:
            if stout:
                print(stout)
            if stderr:
                print_error(stderr)


if __name__ == "__main__":
    run_repl()
