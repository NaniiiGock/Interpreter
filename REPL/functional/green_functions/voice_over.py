from subprocess import Popen, PIPE
from ..BaseClassFunction import GreenFunction


class TellNumberUnreadMessages(GreenFunction):
    @staticmethod
    def run():
        """
        Tells the number of unread messages.
        :return:
        """
        scpt = '''
on isVoiceOverRunning()
	set isRunning to false
	tell application "System Events"
		set isRunning to (name of processes) contains "VoiceOver"
	end tell
	return isRunning
end isVoiceOverRunning

on isVoiceOverRunningWithAppleScript()
	if isVoiceOverRunning() then
		set isRunningWithAppleScript to true
		
		-- is AppleScript enabled on VoiceOver --
		tell application "VoiceOver"
			try
				set x to bounds of vo cursor
			on error
				set isRunningWithAppleScript to false
			end try
		end tell
		return isRunningWithAppleScript
	end if
	return false
end isVoiceOverRunningWithAppleScript

on unreadMailCount()
	tell application "Mail"
		set unreadCount to 0 as number
		set unreadCount to (unread count of inbox) + unreadCount
		return unreadCount
	end tell
end unreadMailCount

set unreadString to ""
set unreadCount to unreadMailCount()

if unreadCount is equal to 1 then
	set unreadString to unreadCount & " unread message" as string
else
	set unreadString to unreadCount & " unread messages" as string
end if


if isVoiceOverRunningWithAppleScript() then
	tell application "VoiceOver"
		output unreadString
	end tell
else
	say unreadString
	delay 2
end if
    '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr