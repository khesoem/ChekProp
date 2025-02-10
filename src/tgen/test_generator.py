from src.config import *
from src.llm.gemini import GeminiFlashLite2
from src.llm.invocation import Prompt

class TestGenerator:
    def __init__(self, model: str, improvement_iterations: int, prompt_type: PromptType,
                 read_from_cache: bool = True, save_to_cache: bool = True):
        self.model = model
        self.improvement_iterations = improvement_iterations
        self.prompt_type = prompt_type
        self.read_from_cache = read_from_cache
        self.save_to_cache = save_to_cache

    def generate_pbt_gemini(self, root_dir: str, src_file: str, src_class: str,
                            test_file: str, test_methods: str) -> str:
        gemini = GeminiFlashLite2(read_from_cache=self.read_from_cache, save_to_cache=self.save_to_cache)

        return gemini.get_response(Prompt([Prompt.Message("user", "What year is now?")])).samples[0].content

    def generate_pbt(self, root_dir: str, src_file: str, src_class: str, test_file: str, test_methods: str) -> str:
        match self.model:
            case 'google/gemini-2.0-flash-lite-preview-02-05:free':
                return self.generate_pbt_gemini(root_dir, src_file, src_class, test_file, test_methods)

            case _:
                raise ValueError(f"Model {self.model} is not supported")