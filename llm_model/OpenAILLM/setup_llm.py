import os

import litellm

from ..utils.debug_utils import print_basic_response_info, print_detailed_choices_info, calculate_and_update_cost

def configure_env():
    """
    Configures the environment for LiteLLM by setting the OpenAI API key.
    You should have .env file in your project root directory with the following content:
    OPENAI_API_KEY=your-openai-api-key
    :return:
    """
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def prepare_messages_for_litellm(prompt, language):
    """
    Prepares messages for LiteLLM to generate code.

    :param prompt: The user's prompt for code generation.
    :param language: The programming language ('python', 'shell', 'applescript').
    :return: A list of messages formatted for LiteLLM.
    """
    messages = []

    # System message to set the context
    system_message = {
        "role": "system",
        "content": f"Generate {language} code for the following task:"
    }
    messages.append(system_message)

    # User message with the actual prompt
    user_message = {
        "role": "user",
        "content": prompt
    }
    messages.append(user_message)

    return messages


def generate_code_with_litellm(prompt, language):
    """
    Generates code using LiteLLM and OpenAI API.

    :param prompt: Basic prompt for code generation.
    :param language: The programming language ('python', 'shell', 'applescript').
    :return: Generated code as a string.
    """
    configure_env()

    # Prepare messages for LiteLLM
    messages = prepare_messages_for_litellm(prompt, language)

    # Set up LiteLLM parameters
    params = {
        "model": "code-davinci-002",  # or another suitable model
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.5,
        # Add any other optional parameters as needed
    }

    # Generate code using LiteLLM
    try:
        response = litellm.completion(**params)
        print_basic_response_info(response)
        print_detailed_choices_info(response)
        calculate_and_update_cost(response)
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Example usage
if __name__ == "__main__":
    prompt = "a script to list all files in the current directory"  # Example prompt
    language = "python"  # Can be 'python', 'shell', or 'applescript'

    generated_code = generate_code_with_litellm(prompt, language)
    print("Generated Code:\n", generated_code)
