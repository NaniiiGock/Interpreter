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

    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))
    return p.returncode, stdout, stderr


def run_scripts(code: str, language: str):
    if language == 'python':
        return run_python_script(code)
    if language == 'shell' or language == 'bash':
        return run_shell_script(code)
    if language == 'osascript' or language == 'applescript':
        return run_applescript(code)


def run_python_script(code: str):
    return run_script(code, 'python', '.py')


def run_shell_script(code: str):
    return run_script(code, 'sh', '.sh')


def run_applescript(code: str):
    return run_script(code, 'osascript', '.scpt')
