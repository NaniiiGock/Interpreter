from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import GreenFunction
import asyncio


class ComposeEmail(GreenFunction):
    @staticmethod
    def get_exec_description():
        return "Composing an email..."

    @staticmethod
    async def run_async(recipient_name: str, recipient_address: str, subject: str, body: str):
        """
        Asynchronously composes an email.
        :param recipient_name: Name of the email recipient.
        :param recipient_address: Email address of the recipient.
        :param subject: Subject of the email.
        :param body: Body of the email.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
        set recipientName to "{recipient_name}"
        set recipientAddress to "{recipient_address}"
        set theSubject to "{subject}"
        set theContent to "{body}"
        tell application "Mail"
            activate	
            set theMessage to make new outgoing message with properties {{subject:theSubject, content:theContent, visible:true}}
            tell theMessage
                make new to recipient with properties {{name:recipientName, address:recipientAddress}}
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
    def run(recipient_name: str, recipient_address: str, subject: str, body: str):
        """
        Composes an email.
        :param recipient_name:
        :param recipient_address:
        :param subject:
        :param body:
        :return:
        """
        scpt = f'''
        set recipientName to "{recipient_name}"
        set recipientAddress to "{recipient_address}"
        set theSubject to "{subject}"
        set theContent to "{body}"
        tell application "Mail"	
            set theMessage to make new outgoing message with properties {{subject:theSubject, content:theContent, visible:true}}
            tell theMessage
                make new to recipient with properties {{name:recipientName, address:recipientAddress}}
            end tell
        end tell
        '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(ComposeEmail.run_async("test", "test", "test", "test"))

    # Do some other stuff while run_async is running
    print("Doing other things while composing email...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
    # TellCurrentDatetime.run()

