import argparse
import logging
import src.config as conf
from datetime import datetime
from src.config import PromptType
from src.tgen.test_generator import TestGenerator

logging.basicConfig(filename='logs/logging_{:%Y-%m-%d-%H-%M}.log'.format(datetime.now()),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--root_dir",
        help="Absolute path to the rood directory",
        required=True,
    )

    parser.add_argument(
        "-sf",
        "--src_file",
        help="Path to the source file to be tested, relative to the root",
        required=True,
    )

    parser.add_argument(
        "-sc",
        "--src_class",
        help="Name of the class for which PBT should be generated",
        required=True
    )

    parser.add_argument(
        "-tf",
        "--test_file",
        help="Path to the sample unit test file",
        required=False,
    )

    parser.add_argument(
        "-tm",
        "--test_methods",
        help="List of sample unit tests, separated by ;",
        required=False,
    )

    parser.add_argument(
        "-it",
        "--improvement_iterations",
        type=int,
        choices=range(0, conf.llm['max-iterations'] + 1),
        default=conf.llm['default-improvement-iterations'],
        help="How many improvement iterations to be used",
        required=False
    )

    parser.add_argument(
        "-pt",
        "--prompt_type",
        type=PromptType,
        choices=list(PromptType),
        default=PromptType.SIMPLE,
        help="Prompt type to be used",
        required=False
    )

    parser.add_argument(
        "-md",
        "--model",
        choices=list(conf.llm['valid-models']),
        default='google/gemini-2.0-flash-lite-preview-02-05:free',
        help="Model to be used",
        required=False
    )

    parser.add_argument(
        "-rc",
        "--read_from_cache",
        type=bool,
        default=True,
        help="Whether to read the invocation from cache",
        required=False
    )

    parser.add_argument(
        "-sv",
        "--save_to_cache",
        type=bool,
        default=True,
        help="Whether to save the invocation to cache",
        required=False
    )

    args = parser.parse_args()

    return (args.root_dir, args.src_file, args.src_class, args.test_file, args.test_methods,
            args.improvement_iterations, args.prompt_type, args.model, args.read_from_cache, args.save_to_cache)


def main() -> None:

    (root_dir, src_file, src_class, test_file, test_methods, improvement_iterations, prompt_type, model,
        read_from_cache, save_to_cache) = get_args()

    logging.info(f"Running with root_dir: {root_dir}, src_file: {src_file}, src_class: {src_class},"
                 f" test_file: {test_file}, test_methods: {test_methods}, prompt_type: {prompt_type},"
                    f" model: {model}, improvement_iterations: {improvement_iterations},"
                    f" read_from_cache: {read_from_cache}, save_to_cache: {save_to_cache}")

    test_generator = TestGenerator(model, improvement_iterations, prompt_type, read_from_cache, save_to_cache)
    print(test_generator.generate_pbt(root_dir, src_file, src_class, test_file, test_methods))

if __name__ == "__main__":
    main()
