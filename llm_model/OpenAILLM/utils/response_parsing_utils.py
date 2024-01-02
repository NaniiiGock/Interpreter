import re

def parse_chunk_language(chunk_text: str):
    """
    Parses the language of a chunk of text.

    :param chunk_text: A chunk of text.
    :return: extention.
    """

    chunk_text = chunk_text.lower()
    if chunk_text.startswith("<python>") or chunk_text.startswith("python"):
        return "py"
    elif chunk_text.startswith("<shell>") or chunk_text.startswith("shell"):
        return "sh"
    elif chunk_text.startswith("<applescript>") or chunk_text.startswith("applescript"):
        return "applescript"
    elif python_regex := re.search(r"python", chunk_text, re.DOTALL):
        return "py"
    elif shell_regex := re.search(r"shell", chunk_text, re.DOTALL):
        return "sh"
    elif applescript_regex := re.search(r"applescript", chunk_text, re.DOTALL):
        return "applescript"
    else:
        return "txt"