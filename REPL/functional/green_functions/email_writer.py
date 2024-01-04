from subprocess import Popen, PIPE
from ..BaseClassFunction import GreenFunction


class ComposeEmail(GreenFunction):
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
