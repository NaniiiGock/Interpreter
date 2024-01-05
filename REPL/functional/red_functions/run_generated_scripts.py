from subprocess import Popen, PIPE
from pathlib import Path
import os
from REPL.functional.BaseClassFunction import RedFunction
import asyncio


class ScriptExecution(RedFunction):

    @staticmethod
    async def run_async(language: str, code: str):
        if not check_language(language):
            return None, None, f"{language} programming language is not supported"
        command = None
        script_extension = None
        if language in ['python']:
            command = 'python'
            script_extension = '.py'
        elif language in ['shell', 'bash']:
            command = 'sh'
            script_extension = '.sh'
        elif language in ['osascript', 'applescript']:
            command = 'osascript'
            script_extension = '.scpt'

        return await asyncio.get_event_loop().run_in_executor(
            None, run_script, code, command, script_extension
        )

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


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(ScriptExecution.run_async('python', 'import time\ntime.sleep(10)\nprint("hello")'))

    # Do some other stuff while run_async is running
    print("Doing other things while running script starts...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
