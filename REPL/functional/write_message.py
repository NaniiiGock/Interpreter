from subprocess import Popen, PIPE


def message_by_phone_number(phone_number: str, body: str):
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


def message_by_contact_name(name: str, body: str):
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
