import os

import litellm

from debug_utils import print_basic_response_info, print_detailed_choices_info, calculate_and_update_cost


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
                    "or AppleScript for the following task. Provide the response in a code block "
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
    print("Generated Code:\n", generated_code)
