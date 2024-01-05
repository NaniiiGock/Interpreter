from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import GreenFunction
import asyncio


class TellNumberUnreadMessages(GreenFunction):
    @staticmethod
    async def run_async():
        """
        Asynchronously tells the number of unread messages in the Mail app.
        :return: Execution result as a dictionary.
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

async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(TellNumberUnreadMessages.run_async())

    # Do some other stuff while run_async is running
    print("Doing other things while telling number of unread messages...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
    # TellCurrentDatetime.run()
