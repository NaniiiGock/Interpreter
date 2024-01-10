from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import RedFunction
import asyncio


class MessageByPhoneNumber(RedFunction):
    @staticmethod
    def get_exec_description():
        return "Sending message by phone number..."

    @staticmethod
    async def run_async(phone_number: str, body: str):
        """
        Asynchronously sends a message to a phone number using iMessage.
        :param phone_number: The phone number to send the message to.
        :param body: The body of the message.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
        tell application "Messages"
            set targetService to 1st account whose service type = iMessage
            set targetBuddy to participant "{phone_number}" of targetService
            send "{body}" to targetBuddy
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
    def get_confirmation_message(phone_number: str, body: str):
        return f"Confirm sending message to phone number: {phone_number} with text: {body}."

    @staticmethod
    def run(phone_number: str, body: str):
        """
        Sends a message to a phone number.
        :param phone_number:
        :param body:
        :return:
        """
        scpt = f'''
        tell application "Messages"
            set targetService to 1st account whose service type = iMessage
            set targetBuddy to participant "{phone_number}" of targetService
            send "{body}" to targetBuddy
        end tell
        '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


class MessageByContactName(RedFunction):
    @staticmethod
    def get_exec_description():
        return "Sending message by contact name..."

    @staticmethod
    async def run_async(name: str, body: str):
        """
        Asynchronously sends a message to a contact name using iMessage.
        :param name: The contact name.
        :param body: The body of the message.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
        tell application "Contacts"
            set thePerson to first person whose name is "{name}"
            set phoneNumber to value of first phone of thePerson
            quit
        end tell
        
        tell application "Messages"
            set targetService to 1st account whose service type = iMessage
            set targetBuddy to participant phoneNumber of targetService
            send "{body}" to targetBuddy
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
    def get_confirmation_message(name: str, body: str):
        return f"Confirm sending message to name: {name} with text: {body}."

    @staticmethod
    def run(name: str, body: str):
        """
        Sends a message to a contact name.
        :param name:
        :param body:
        :return:
        """
        scpt = f'''
        tell application "Contacts"
            set thePerson to first person whose name is "{name}"
            set phoneNumber to value of first phone of thePerson
        end tell
        
        tell application "Messages"
            set targetService to 1st account whose service type = iMessage
            set targetBuddy to participant phoneNumber of targetService
            send "{body}" to targetBuddy
        end tell
        '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(MessageByContactName.run_async('Anastasiia 🌸', 'Writing async message to you, honey!'))

    # Do some other stuff while run_async is running
    print("Doing other things while sending message starts...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
