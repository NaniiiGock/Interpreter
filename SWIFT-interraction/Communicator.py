from response_parser import ResponseParser
from StatusCodes import StatusCode


class Communicator:
    @staticmethod
    def swift_input(uuid, user_input):
        """
        Function that will be called from swift to send user input to the LLM
        :param uuid:
        :param user_input:
        :return:
        """
        llm_message = None  # <<<Placeholder for async call to LLM>>> #
        status_code, response = ResponseParser.parse_response_object(llm_message)

        # <<<Placeholder for writing response into DB>>> #

        if status_code == StatusCode.RAW_TEXT:
            return uuid, response.content, status_code

        elif status_code == StatusCode.SAFE:
            # <<<Placeholder for async execution>>> #
            return uuid, ResponseParser.get_func_class(response.func_name).get_exec_description(), status_code
        elif status_code == StatusCode.CONFIRM:
            return uuid, \
                ResponseParser.get_func_class(response.func_name).get_confirmation_message(
                    **response.get_formatted_args()
                ), status_code


