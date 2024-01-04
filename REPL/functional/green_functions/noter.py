from subprocess import Popen, PIPE
from ..BaseClassFunction import GreenFunction


class MakeNote(GreenFunction):
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
