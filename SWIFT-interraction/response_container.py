import json


class LLMResponse:
    def __init__(self):
        self.content = None
        self.func_name = None
        self.func_args = None

    def get_type(self):
        return "text" if self.content else "func"

    def get_args(self):
        return self.func_args

    def get_formatted_args(self):
        return json.loads(self.func_args)

    def set_response(self, content, func_name, func_args):
        self.content = content
        self.func_name = func_name
        self.func_args = func_args

    def set_content(self, content):
        self.content = content

    def set_func_name(self, func_name):
        self.func_name = func_name

    def set_func_args(self, func_args):
        self.func_args = func_args
