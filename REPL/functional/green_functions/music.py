from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import GreenFunction
import asyncio


class TurnMusic(GreenFunction):

    @staticmethod
    async def run_async(name: str):
        """
        Turns on music.
        :param name:
        :return:
        """
        scpt = f'''
        tell application "Music"
            play track "{name}"
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

        print("run")
        # Return the results
        return {
            'returncode': process.returncode,
            'stdout': stdout_str,
            'stderr': stderr_str
        }

    @staticmethod
    def construct_script(name: str):
        return f'''
        tell application "Music"
            play track "{name}"
        end tell
        '''

    @staticmethod
    def run(name: str):
        """
        Turns on music.
        :param name:
        :return:
        """
        scpt = f'''
        tell application "Music"
            play track "{name}"
        end tell
        '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(TurnMusic.run_async('You Drive My Four Wheel Coffin'))

    # Do some other stuff while run_async is running
    print("Doing other things while music starts...")
    await asyncio.sleep(2)  # Simulate some other work

    # Now, wait for the run_async task to complete if it hasn't already
    result = await task
    print("main")
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
