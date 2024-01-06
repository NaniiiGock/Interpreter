import os
import asyncio
import litellm
from llm_model.OpenAILLM.utils.debug_utils import (
    print_basic_response_info,
    print_detailed_choices_info,
    calculate_and_update_cost
)
import warnings
from llm_model.OpenAILLM.setup_llm import get_tools

warnings.filterwarnings('ignore')


class LiteLLMClient:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.model_name = model_name
        self.configure_env()

    @staticmethod
    def configure_env():
        """
        Configures the environment for LiteLLM by setting the OpenAI API key.
        """
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def prepare_messages_for_litellm(prompt):
        """
        Prepares messages for LiteLLM to generate code.

        :param prompt: The user's prompt for code generation.
        :return: A list of messages formatted for LiteLLM.
        """
        messages = [
            {
                "role": "system",
                "content": "You are a code generation assistant. Generate code only in Python, Shell, "
                           "or AppleScript for the following task"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        return messages

    @staticmethod
    def get_tools():
        """
        Returns a list of tools that can be used for code generation.
        """
        return get_tools()

    def support_func_calls(self):
        """
        Checks if the model supports function calls.
        """
        return self.model_name in {
            "gpt-4", "gpt-4-1106-preview", "gpt-4-0613", "gpt-3.5-turbo",
            "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0613"
        }

    def generate_params(self, prompt):
        """
        Generates the parameters for the LiteLLM API call.
        """
        messages = self.prepare_messages_for_litellm(prompt)
        params = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 250,
            "temperature": 0.8
        }
        if self.support_func_calls():
            params.update({
                "tools": self.get_tools(),
                "tool_choice": "auto"
            })
        return params

    def get_response(self, prompt):
        """
        Synchronously generates a response using LiteLLM

        :param prompt: Basic prompt for response generation.
        :return: Generated response as a string.
        """
        params = self.generate_params(prompt)
        try:
            response = litellm.completion(**params)
            print_basic_response_info(response)
            print_detailed_choices_info(response)
            calculate_and_update_cost(response)
            return response['choices'][0]['message']
        except Exception as e:
            return f"An error occurred: {str(e)}"

    async def get_response_async(self, prompt):
        """
        Asynchronously generates a response using LiteLLM

        :param prompt: Basic prompt for response generation.
        :return: Generated response as a string.
        """
        params = self.generate_params(prompt)
        try:
            response = await litellm.completion(**params)
            print_basic_response_info(response)
            print_detailed_choices_info(response)
            calculate_and_update_cost(response)
            return response['choices'][0]['message']
        except Exception as e:
            return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    client = LiteLLMClient("gpt-3.5-turbo")
    response = client.get_response("Write a poem")
    print(response)


# For async, you would use:
# async def main():
#     response = await client.get_response_async("Write a Python function")
#     print(response)
#
# asyncio.run(main())
