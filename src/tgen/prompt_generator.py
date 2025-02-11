import ast

from src.config import PromptType
from src.llm.invocation import Prompt
from os import path
from src.config import llm

class PromptGenerator:
    def __init__(self, prompt_type: PromptType, temp: float, sample_size: int, model: str):
        self.prompt_type = prompt_type
        with open(path.join(llm['prompt-template-dir'], f'{prompt_type}.txt'), 'r') as f:
            self.prompt_template = f.read()
        self.temp = temp
        self.sample_size = sample_size
        self.model = model

    def get_initial_prompt_txt(self, cl_code: str, class_name: str, unittests_code: str) -> str:
        return self.prompt_template.format(class_name=class_name, class_code=cl_code, unittests_code=unittests_code)

    def generate_initial_prompt(self, root_dir: str, src_file: str, class_name: str, test_file: str,
                                test_methods: str) -> Prompt:
        with open(path.join(root_dir, src_file), 'r') as f:
            node = ast.parse(f.read())
            cl = next(n for n in node.body if isinstance(n, ast.ClassDef) and n.name == class_name)
            cl_code = ast.unparse(cl)

        if test_file:
            with open(path.join(root_dir, test_file), 'r') as f:
                node = ast.parse(f.read())
                unittests = [n for n in node.body if isinstance(n, ast.FunctionDef)
                                and (not test_methods or n.name in test_methods)]
                unittests_code = '\n'.join(ast.unparse(test) for test in unittests)

        prompt_txt = self.get_initial_prompt_txt(cl_code, class_name, unittests_code)

        return Prompt([Prompt.Message("user", prompt_txt)], self.temp, self.sample_size, self.model)