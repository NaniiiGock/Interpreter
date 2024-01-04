from subprocess import Popen, PIPE
from ..BaseClassFunction import RedFunction


class CallByPhoneNumber(RedFunction):
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
