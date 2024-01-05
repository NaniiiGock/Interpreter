from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import RedFunction
import asyncio


class CallByPhoneNumber(RedFunction):
    @staticmethod
    async def run_async(phone_number: str):
        """
        Asynchronously makes a call to a phone number using FaceTime.
        :param phone_number: The phone number to call.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
        set phone to "{phone_number}" 
        open location "facetime://" & phone & "?audio=yes"

        tell application "FaceTime" to activate
        tell application "System Events" to tell application process "FaceTime"
            set frontmost to true 
                repeat until window "FaceTime" exists
                delay 0.1
            end repeat
            tell window "FaceTime" to tell button "Call" to perform action "AXPress"
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
    def get_confirmation_message(phone_number: str):
        return f"Confirm making a call by phone number: {phone_number}."

    @staticmethod
    def run(phone_number: str):
        """
        Calls someone.
        :param phone_number:
        :return:
        """
        scpt = f'''
        set phone to "{phone_number}" 
        open location "facetime://" & phone & "?audio=yes"
    
        tell application "FaceTime" to activate
        tell application "System Events" to tell application process "FaceTime"
            set frontmost to true 
                repeat until window "FaceTime" exists
                delay 0.1
            end repeat
            tell window "FaceTime" to tell button "Call" to perform action "AXPress"
        end tell
        '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


class CallByName(RedFunction):
    @staticmethod
    async def run_async(name: str):
        """
        Asynchronously makes a call to a contact name using FaceTime.
        :param name: The name of the contact.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
        set contactName to "{name}" -- Replace with the name of your contact
        tell application "Contacts"
            set thePerson to first person whose name is contactName
            set phoneNumber to value of first phone of thePerson
        end tell
        
        set phone to phoneNumber
        tell application "FaceTime"
            activate
            open location "facetime://" & phone & "?audio=yes"
        end tell
        
        tell application "System Events" to tell application process "FaceTime"
            set frontmost to true
            repeat until window "FaceTime" exists
                delay 0.1
            end repeat
            tell window "FaceTime" to tell button "Call" to perform action "AXPress"
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
    def get_confirmation_message(name: str):
        return f"Confirm making a call by name: {name}."

    @staticmethod
    def run(name: str):
        """
        Calls someone by name.
        :param name:
        :return:
        """
        scpt = f'''
        set contactName to "{name}" -- Replace with the name of your contact
        tell application "Contacts"
            set thePerson to first person whose name is contactName
            set phoneNumber to value of first phone of thePerson
        end tell
        
        set phone to phoneNumber
        tell application "FaceTime"
            activate
            open location "facetime://" & phone & "?audio=yes"
        end tell
        
        tell application "System Events" to tell application process "FaceTime"
            set frontmost to true
            repeat until window "FaceTime" exists
                delay 0.1
            end repeat
            tell window "FaceTime" to tell button "Call" to perform action "AXPress"
        end tell
        '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(CallByPhoneNumber.run_async('0972045140'))

    # Do some other stuff while run_async is running
    print("Doing other things while calling starts...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
