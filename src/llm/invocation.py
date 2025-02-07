from src.config import PromptType


class Prompt:
    def __init__(self, prompt_type: PromptType):
        self.prompt_type = prompt_type

    def hash(self):
        return hash(self.prompt_type)

class Invocation:
    def __init__(self, prompt: Prompt, response):
        self.prompt = prompt
        self.response = response