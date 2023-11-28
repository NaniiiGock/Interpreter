import os
import subprocess
import litellm
import re
from debug_utils import print_basic_response_info, print_detailed_choices_info, calculate_and_update_cost
import warnings
warnings.filterwarnings('ignore')


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


def write_to_file(content: str, extention: str, filename="generated_code"):
    """
    Writes the generated code to a file.

    :param content: The generated code.
    :param extention: The extention of the file.
    :param filename: The name of the file.
    :return: filename: The name of the file with the extention.
    """
    content = content.split("\n", 1)[1]
    with open(f'{filename}.{extention}', "w") as f:
        f.write("\n".join(content))
    return f'{filename}.{extention}'


def execute_generated_code(filename: str, extent: str):
    """
    Executes the generated code.

    :param filename: The name of the file containing the generated code.
    :param extent: The extention of the file.
    :return: The output of the generated code.
    """
    if extent == "py":
        output = subprocess.run([f'python {filename}'])
        return output.stdout.decode("utf-8")
    elif extent == "sh":
        output = subprocess.run([f'bash {filename}'])
        return output.stdout.decode("utf-8")
    elif extent == "applescript":
        output = subprocess.run([f'osascript {filename}'])
        return output.stdout.decode("utf-8")
    else:
        return "Error: Invalid extention"


def configure_env():
    """
    Configures the environment for LiteLLM by setting the OpenAI API key.
    You should have .env file in your project root directory with the following content:
    OPENAI_API_KEY=your-openai-api-key
    :return:
    """
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def prepare_messages_for_litellm(prompt):
    """
    Prepares messages for LiteLLM to generate code.

    :param prompt: The user's prompt for code generation.
    :return: A list of messages formatted for LiteLLM.
    """
    messages = []

    # System message to set the context and instructions
    system_message = {
        "role": "system",
        "content": ("You are a code generation assistant. Generate code only in Python, Shell, "
                    "or AppleScript for the following task. Write only code without explanation. Provide the response "
                    "in a code block"
                    "with the language specified at the start, like so: "
                    "`<language>\\n<code>`")
    }
    messages.append(system_message)

    example_message = {
        'role': 'user',
        "content": "Play song You drive my four wheel coffin"
    }
    messages.append(example_message)

    example_response = {
        'role': 'assistant',
        'content': """<applescript>
        tell application "Music"
            play track "Last Christmas"
        end tell
        <code>"""
    }
    messages.append(example_response)
    # User message with the actual prompt
    user_message = {
        "role": "user",
        "content": prompt
    }
    messages.append(user_message)

    return messages


def generate_code_with_litellm(prompt):
    """
    Generates code using LiteLLM and OpenAI API.

    :param prompt: Basic prompt for code generation.
    :param language: The programming language ('python', 'shell', 'applescript').
    :return: Generated code as a string.
    """
    configure_env()

    # Prepare messages for LiteLLM
    messages = prepare_messages_for_litellm(prompt)

    # Set up LiteLLM parameters
    params = {
        "model": "gpt-3.5-turbo-instruct",  # or another suitable model
        "messages": messages,
        "max_tokens": 250,
        "temperature": 0.8,
        # Add any other optional parameters as needed
    }

    # Generate code using LiteLLM
    try:
        response = litellm.completion(**params)
        print_basic_response_info(response)
        print_detailed_choices_info(response)
        calculate_and_update_cost(response)

        # Accessing the generated content correctly
        generated_content = response['choices'][0]['message']['content'].strip()
        return generated_content
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Example usage
if __name__ == "__main__":
    prompt = "Play You drive my four wheel coffin song"  # Example prompt
    # language = "python"  # Can be 'python', 'shell', or 'applescript'
    configure_env()
    generated_code = generate_code_with_litellm(prompt)
    language = parse_chunk_language(generated_code)
    file_name = write_to_file(generated_code, language)
    print("Generated Code:\n", generated_code)
    output = execute_generated_code(file_name, language)
    print("Output:\n", output)

