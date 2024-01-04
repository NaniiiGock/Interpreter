from subprocess import Popen, PIPE
from ..BaseClassFunction import GreenFunction


class OpenApp(GreenFunction):
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
