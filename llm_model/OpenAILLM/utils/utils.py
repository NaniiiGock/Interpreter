import subprocess


def write_to_file(content: str, extention: str, filename="generated_code"):
    """
    Writes the generated code to a file.

    :param content: The generated code.
    :param extention: The extention of the file.
    :param filename: The name of the file.
    :return: filename: The name of the file with the extention.
    """

    content = content.replace("<python>", "").replace("<shell>", "").replace("<applescript>", "")
    with open(f'{filename}.{extention}', "w") as f:
        f.write(content)
    return f'{filename}.{extention}'


def execute_generated_code(filename: str, extent: str):
    """
    Executes the generated code.

    :param filename: The name of the file containing the generated code.
    :param extent: The extention of the file.
    :return: The output of the generated code.
    """
    if extent == "py":
        output = subprocess.run(['python', filename])
        # return output.stdout.decode("utf-8")
    elif extent == "sh":
        output = subprocess.run([f'bash {filename}'])
        return output.stdout.decode("utf-8")
    elif extent == "applescript":
        output = subprocess.run([f'osascript {filename}'])
        return output.stdout.decode("utf-8")
    else:
        return "Error: Invalid extension"
