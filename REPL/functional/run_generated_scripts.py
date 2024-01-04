from subprocess import Popen, PIPE
import os


def write_to_file(path, content):
    with open(path, 'w') as file:
        file.write(content)


def clear_file(path):
    os.remove(path)


def run_script(script_content: str, command: str, script_extension: str):
    SCRIPT_PATH = f'./temp/script{script_extension}'

    write_to_file(SCRIPT_PATH, script_content)
    p = Popen([command, SCRIPT_PATH], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    clear_file(SCRIPT_PATH)
    return p.returncode, stdout, stderr


def run_scripts(code: str, language: str):
    if language == 'python':
        return run_script(code, 'python', '.py')
    if language == 'shell' or language == 'bash':
        return run_script(code, 'sh', '.sh')
    if language == 'osascript' or language == 'applescript':
        return run_script(code, 'osascript', '.scpt')

    return "there's no such language"


def check_language(language):
    return language in ['python', 'shell', 'bash', 'applescript', 'osascript']

