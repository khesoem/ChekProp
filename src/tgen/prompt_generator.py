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

    def get_initial_prompt_txt(self, mod_name: str, cl_code: str, class_name: str, unittests_code: str) -> str:
        if (('mod_name' in self.prompt_template and not mod_name)
                or ('class_code' in self.prompt_template and not cl_code)
                or ('unittests_code' in self.prompt_template and not unittests_code)
                or ('class_name' in self.prompt_template and not class_name)):
            raise ValueError("Prompt template is missing required values")

        return self.prompt_template.format(module_name=mod_name, class_name=class_name, class_code=cl_code,
                                           unittests_code=unittests_code)

    def generate_initial_prompt(self, root_dir: str, src_file: str, class_name: str, test_file: str,
                                test_methods: str) -> Prompt:
        mod_name = src_file.replace('.py', '').replace('/', '.')

        with open(path.join(root_dir, src_file), 'r') as f:
            node = ast.parse(f.read())
            imports = [n for n in node.body if isinstance(n, ast.Import) or isinstance(n, ast.ImportFrom)]
            cl = next(n for n in node.body if isinstance(n, ast.ClassDef) and n.name == class_name)
            cl_code = '\n'.join(ast.unparse(im) for im in imports)
            cl_code += '\n' + ast.unparse(cl)

        if test_file:
            with open(path.join(root_dir, test_file), 'r') as f:
                node = ast.parse(f.read())
                imports = [n for n in node.body if isinstance(n, ast.Import) or isinstance(n, ast.ImportFrom)]
                unittests = [n for n in node.body if isinstance(n, ast.FunctionDef)
                                and (not test_methods or n.name in test_methods)]
                unittests_code = '\n'.join(ast.unparse(im) for im in imports)
                unittests_code += '\n' + '\n'.join(ast.unparse(test) for test in unittests)

        prompt_txt = self.get_initial_prompt_txt(mod_name, cl_code, class_name, unittests_code)

        return Prompt([Prompt.Message("user", prompt_txt)], self.temp, self.sample_size, self.model)