from subprocess import Popen, PIPE


def tell_current_datetime():
    """
    Tells the current date and time.
    :return:
    """
    scpt = f'''
    set theDialogText to "The curent date and time is " & (current date) & "."
    display dialog theDialogText
    '''
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(scpt)
    return p.returncode, stdout, stderr
