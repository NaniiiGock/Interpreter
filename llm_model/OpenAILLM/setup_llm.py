import os
import litellm
from llm_model.OpenAILLM.utils.debug_utils import print_basic_response_info, print_detailed_choices_info, \
    calculate_and_update_cost
import warnings

warnings.filterwarnings('ignore')

# litellm.set_verbose = True


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
        "content": "You are a code generation assistant. Generate code only in Python, Shell, "
                   "or AppleScript for the following task"
    }
    messages.append(system_message)

    # example_message = {
    #     'role': 'user',
    #     "content": "Play song You drive my four wheel coffin"
    # }
    # messages.append(example_message)
    #
    # example_response = {
    #     'role': 'assistant',
    #     'content': """<applescript>
    #     tell application "Music"
    #         play track "Last Christmas"
    #     end tell
    #     <\code>"""
    # }
    # messages.append(example_response)

    # User message with the actual prompt
    user_message = {
        "role": "user",
        "content": prompt
    }
    messages.append(user_message)

    return messages


def get_tools():
    """
    Returns a list of tools that can be used for code generation.
    """
    tools = [
        {
            'type': 'function',
            'function': {
                'name': 'turn_music',
                'description': 'Turns the music on',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'The name of the song to play'
                        }
                    },
                    'required': ['name']
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'tell_current_datetime',
                'description': 'Tells the current date and time',
                'parameters': {
                    'type': 'object',
                    'properties': {
                    },
                    'required': []
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'open_app',
                'description': 'Opens an app',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'The name of the app to open'
                        }
                    },
                    'required': ['name']
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'call_by_phone_number',
                'description': 'Calls someone by phone number',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'phone_number': {
                            'type': 'string',
                            'description': 'The phone number to call'
                        }
                    },
                    'required': ['phone_number']
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'call_by_name',
                'description': 'Calls someone by name',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'The name of the person to call'
                        }
                    },
                    'required': ['name']
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'schedule_command',
                'description': 'Schedules a command using crontab',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'frequency': {
                            'type': 'string',
                            'description': 'Frequency to run the command with crontab'
                        },
                        'command': {
                            'type': 'string',
                            'description': 'Command to schedule'
                        }
                    },
                    'required': ['frequency', 'command']
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'remove_scheduled_command',
                'description': 'Remove command that was scheduled with crontab',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'frequency': {
                            'type': 'string',
                            'description': 'Frequency for command to with crontab'
                        },
                        'command': {
                            'type': 'string',
                            'description': 'Command to remove'
                        }
                    },
                    'required': ['frequency', 'command']
                }
            }
        }
    ]

    return tools


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
        "model": "gpt-3.5-turbo",  # or another suitable model
        "messages": messages,
        "tools": get_tools(),
        "tool_choice": "auto",
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
        generated_content = response['choices'][0]['message']
        return generated_content
    except Exception as e:
        return f"An error occurred: {str(e)}"
