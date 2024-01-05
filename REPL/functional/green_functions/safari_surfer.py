from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import GreenFunction
import asyncio


class SearchGoogle(GreenFunction):
    @staticmethod
    async def run_async(query: str):
        """
        Asynchronously searches Google with a query using Safari.
        :param query: The search query.
        :return: Execution result as a dictionary.
        """
        scpt = f'''
        set searchQuery to "{query}"

        -- URL encode the search query
        set searchQuery to urlencode(searchQuery)

        -- Define the search engine URL, using Google in this example
        set searchURL to "http://www.google.com/search?q=" & searchQuery

        -- AppleScript commands to interact with Safari
        tell application "Safari"
            -- Make sure Safari is running
            activate
            
            -- Open a new window if no window is open; otherwise, create a new tab in the existing window
            if (count of windows) is 0 then
                make new document
            end if
            
            -- Create a new tab and set it to the search URL
            tell front window
                set current tab to (make new tab with properties {{URL:searchURL}})
            end tell
        end tell

        -- Handler to URL encode text
        on urlencode(theText)
            tell application "Safari"
                return do JavaScript "encodeURIComponent('" & theText & "')" in document 1
            end tell
        end urlencode
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
    def run(query: str):
        """
        Search google with query
        :param query:
        :return:
        """
        scpt = f'''
    set searchQuery to "{query}"

-- URL encode the search query
set searchQuery to urlencode(searchQuery)

-- Define the search engine URL, using Google in this example
set searchURL to "http://www.google.com/search?q=" & searchQuery

-- AppleScript commands to interact with Safari
tell application "Safari"
	-- Make sure Safari is running
	activate
	
	-- Open a new window if no window is open; otherwise, create a new tab in the existing window
	if (count of windows) is 0 then
		make new document
	end if
	
	-- Create a new tab and set it to the search URL
	tell front window
		set current tab to (make new tab with properties {{URL:searchURL}})
	end tell
end tell

-- Handler to URL encode text
on urlencode(theText)
	tell application "Safari"
		return do JavaScript "encodeURIComponent('" & theText & "')" in document 1
	end tell
end urlencode
    '''
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(scpt)
        return p.returncode, stdout, stderr


async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(SearchGoogle.run_async("UCU"))

    # Do some other stuff while run_async is running
    print("Doing other things while browsing...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
    # TellCurrentDatetime.run()
