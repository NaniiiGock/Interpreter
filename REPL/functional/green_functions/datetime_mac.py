from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import GreenFunction
import asyncio


class TellCurrentDatetime(GreenFunction):
    @staticmethod
    async def run_async():
        """
        Asynchronously tells the current date and time.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
            (* 
 Speaks the  date and time of day
 
 Copyright 2008 Apple Inc. All rights reserved.
 
 You may incorporate this Apple sample code into your program(s) without
 restriction.  This Apple sample code has been provided "AS IS" and the
 responsibility for its operation is yours.  You are not permitted to
 redistribute this Apple sample code as "Apple sample code" after having
 made changes.  If you're going to redistribute the code, we require
 that you make it clear that the code was descended from Apple sample
 code, but that you've made changes.
 *)

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

set currentDate to current date
set amPM to "AM"
set currentHour to (currentDate's hours)
set currentMinutes to currentDate's minutes

if (currentHour ≥ 12 and currentHour < 24) then
	set amPM to "PM"
else
	set amPM to "AM"
end if

--  make minutes below 10 sound nice
if currentMinutes < 10 then
	set currentMinutes to ("0" & currentMinutes) as text
end if

--  ensure 0:nn gets set to 12:nn AM
if currentHour is equal to 0 then
	set currentHour to 12
end if

--  readjust for 12 hour time
if (currentHour > 12) then
	set currentHour to (currentHour - 12)
end if

set currentTime to ((currentDate's month) as text) & " " & ((currentDate's day) as text) & ", " & (currentHour as text) & ":" & ((currentMinutes) as text) & " " & amPM as text

if isVoiceOverRunningWithAppleScript() then
	tell application "VoiceOver"
		output currentTime
	end tell
else
	say currentTime
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
        Tells the current date and time.
        :return:
        """
        scpt = f'''
    (* 
 Speaks the  date and time of day
 
 Copyright 2008 Apple Inc. All rights reserved.
 
 You may incorporate this Apple sample code into your program(s) without
 restriction.  This Apple sample code has been provided "AS IS" and the
 responsibility for its operation is yours.  You are not permitted to
 redistribute this Apple sample code as "Apple sample code" after having
 made changes.  If you're going to redistribute the code, we require
 that you make it clear that the code was descended from Apple sample
 code, but that you've made changes.
 *)

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

set currentDate to current date
set amPM to "AM"
set currentHour to (currentDate's hours)
set currentMinutes to currentDate's minutes

if (currentHour ≥ 12 and currentHour < 24) then
	set amPM to "PM"
else
	set amPM to "AM"
end if

--  make minutes below 10 sound nice
if currentMinutes < 10 then
	set currentMinutes to ("0" & currentMinutes) as text
end if

--  ensure 0:nn gets set to 12:nn AM
if currentHour is equal to 0 then
	set currentHour to 12
end if

--  readjust for 12 hour time
if (currentHour > 12) then
	set currentHour to (currentHour - 12)
end if

set currentTime to ((currentDate's month) as text) & " " & ((currentDate's day) as text) & ", " & (currentHour as text) & ":" & ((currentMinutes) as text) & " " & amPM as text

if isVoiceOverRunningWithAppleScript() then
	tell application "VoiceOver"
		output currentTime
	end tell
else
	say currentTime
	delay 2
end if
    '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(TellCurrentDatetime.run_async())

    # Do some other stuff while run_async is running
    print("Doing other things while telling time...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
    # TellCurrentDatetime.run()
