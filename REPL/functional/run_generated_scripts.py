from subprocess import Popen, PIPE
import os
from pathlib import Path


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


def run_scripts(language: str, code: str):
    if language == 'python':
        return run_script(code, 'python', '.py')
    if language == 'shell' or language == 'bash':
        return run_script(code, 'sh', '.sh')
    if language == 'osascript' or language == 'applescript':
        return run_script(code, 'osascript', '.scpt')

    return "there's no such language"


def check_language(language):
    return language in ['python', 'shell', 'bash', 'applescript', 'osascript']

