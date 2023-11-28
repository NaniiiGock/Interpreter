import atexit
import logging
import os

import readline

import llm_model.OpenAILLM.setup_llm as setup_llm
from REPL import REQUESTS_HISTORY_PATH


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

    while True:
        line = input("> ").strip()
        if line == "exit":
            break
        elif line == 'Play "You Drive My Four Wheel Coffin" every day at 7:00':
            os.system(
                "task_sheduler 0 7 * * * osascript -e 'tell application Music to play track You Drive My Four Wheel Coffin'")
            continue
        llm_response = setup_llm.generate_code_with_litellm(line)
        extension = setup_llm.parse_chunk_language(llm_response)
        tmp_filename = "tmp." + extension
        setup_llm.write_to_file(llm_response, extension, tmp_filename)
        setup_llm.execute_generated_code(tmp_filename, llm_response)


if __name__ == "__main__":
    run_repl()
