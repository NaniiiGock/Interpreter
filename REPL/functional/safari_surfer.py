from subprocess import Popen, PIPE


def search_google(query):
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
