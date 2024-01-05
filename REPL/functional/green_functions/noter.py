from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import GreenFunction
import asyncio


class MakeNote(GreenFunction):
    @staticmethod
    async def run_async(note_title: str, note_body: str):
        """
        Asynchronously makes a note.
        :param note_title: Title of the note.
        :param note_body: Body of the note.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
        tell application "Notes"
            activate
            tell account "iCloud"
                tell folder "Notes"
                    make new note with properties {{name:"{note_title}", body:"{note_body}"}}
                end tell
            end tell
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

    @staticmethod
    def run(note_title: str, note_body: str):
        """
        Makes a note.
        :param note_title:
        :param note_body:
        :return:
        """
        scpt = f'''
        tell application "Notes"
            activate
            tell account "iCloud"
                tell folder "Notes"
                    make new note with properties {{name:"{note_title}", body:"{note_body}"}}
                end tell
            end tell
        end tell
        '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(MakeNote.run_async("test", "test"))

    # Do some other stuff while run_async is running
    print("Doing other things while writing note...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
    # TellCurrentDatetime.run()
