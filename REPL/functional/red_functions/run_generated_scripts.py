from subprocess import Popen, PIPE
from pathlib import Path
import os
from ..BaseClassFunction import RedFunction


class ScriptExecution(RedFunction):
    @staticmethod
    def get_confirmation_message(language: str, code: str):
        return f"Confirm executing script with the programing language: {language} and with the next code:" \
               f"\n```" \
               f"\n{code}" \
               f"\n```"

    @staticmethod
    def run(language: str, code: str):
        if language == 'python':
            return run_script(code, 'python', '.py')
        if language == 'shell' or language == 'bash':
            return run_script(code, 'sh', '.sh')
        if language == 'osascript' or language == 'applescript':
            return run_script(code, 'osascript', '.scpt')

        return None, None, f"{language} programming language is not supported"


def write_to_file(path, content):
    with open(path, 'w') as file:
        file.write(content)


def clear_file(path):
    os.remove(path)


def run_script(script_content: str, command: str, script_extension: str):
    script_path = f'./temp/script{script_extension}'
    Path("./temp").mkdir(parents=True, exist_ok=True)

    write_to_file(script_path, script_content)
    p = Popen([command, script_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    clear_file(script_path)
    return p.returncode, stdout, stderr


def check_language(language):
    return language in ['python', 'shell', 'bash', 'applescript', 'osascript']

