from subprocess import Popen, PIPE
from ..BaseClassFunction import RedFunction


class MessageByPhoneNumber(RedFunction):
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
