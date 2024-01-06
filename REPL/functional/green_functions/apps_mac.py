import time
from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import GreenFunction
import asyncio


class OpenApp(GreenFunction):
    @staticmethod
    def get_exec_description():
        return "Opening the app..."

    @staticmethod
    def run(name: str):
        """
        Opens an application.
        :param name:
        :return:
        """
        scpt = f'''
        tell application "{name}"
            activate
        end tell
        '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr

    @staticmethod
    async def run_async(name: str):
        """
        Asynchronously opens an application.
        :param name: The name of the application to open.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
        tell application "{name}"
            activate
        end tell
        '''
        scpt_bytes = scpt.encode('utf-8')

        # Start an AppleScript process
        process = await asyncio.create_subprocess_exec(
            'osascript', '-',
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
        # Send the script bytes and wait for completion
        stdout, stderr = await process.communicate(input=scpt_bytes)

        # Decode stdout and stderr to string if needed
        stdout_str = stdout.decode('utf-8') if stdout else ''
        stderr_str = stderr.decode('utf-8') if stderr else ''

        return {
            'returncode': process.returncode,
            'stdout': stdout_str,
            'stderr': stderr_str
        }


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(OpenApp.run_async('FaceTime'))

    # Do some other stuff while run_async is running
    print("Doing other things while opening app...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())

