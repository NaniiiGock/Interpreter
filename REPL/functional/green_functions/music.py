from subprocess import Popen, PIPE
from ..BaseClassFunction import GreenFunction


class TurnMusic(GreenFunction):
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
