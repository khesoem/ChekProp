from src.config import *
from src.llm.gemini import GeminiFlashLite2
from src.llm.invocation import Prompt
from .prompt_generator import PromptGenerator

class TestGenerator:
    def __init__(self, model: str, improvement_iterations: int, prompt_type: PromptType,
                 temp: float, sample_size: int, read_from_cache: bool, save_to_cache: bool):
        self.model = model
        self.improvement_iterations = improvement_iterations
        self.prompt_type = prompt_type
        self.temp = temp
        self.sample_size = sample_size
        self.read_from_cache = read_from_cache
        self.save_to_cache = save_to_cache

    @staticmethod
    def extract_code_from_llm_response(response: str) -> str:
        return '\n'.join(response.split('```')[-2].strip().split('\n')[1:])

    def generate_pbt_gemini(self, root_dir: str, src_file: str, src_class: str,
                            test_file: str, test_methods: str) -> str:
        gemini = GeminiFlashLite2(read_from_cache=self.read_from_cache, save_to_cache=self.save_to_cache)

        prompt_generator = PromptGenerator(self.prompt_type, self.temp, self.sample_size, self.model)
        initial_prompt = prompt_generator.generate_initial_prompt(root_dir, src_file, src_class, test_file, test_methods)

        gemini_response = gemini.get_response(initial_prompt).samples[0].content
        return self.extract_code_from_llm_response(gemini_response)

    def generate_pbt(self, root_dir: str, src_file: str, src_class: str, test_file: str, test_methods: str) -> str:
        match self.model:
            case 'google/gemini-2.0-flash-lite-preview-02-05:free':
                return self.generate_pbt_gemini(root_dir, src_file, src_class, test_file, test_methods)

            case _:
                raise ValueError(f"Model {self.model} is not supported")