from enum import Enum, auto

class PromptType(Enum):
    SIMPLE = 'SIMPLE'

    def __str__(self):
        return self.value

llm = {
    'llm-invocation-cache-dir': 'cache/llm-invocations'
}