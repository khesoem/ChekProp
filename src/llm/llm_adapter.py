import os, json, logging

import src.config as conf
from src.llm.invocation import Invocation, Prompt


class LLMAdapter:
    def __init__(self):
        self.cache_dir = conf.llm['llm-invocation-cache-dir']

    def load_cache(self, prompt: Prompt):
        cache_file = os.path.join(self.cache_dir, f"{prompt.hash()}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None

    def save_cache(self, invocation: Invocation):
        cache_file = os.path.join(self.cache_dir, f"{invocation.prompt.hash()}.json")
        with open(cache_file, 'w') as f:
            json.dump(invocation, f)