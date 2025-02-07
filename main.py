import argparse
import logging
import src.config as conf
from datetime import datetime
import enum

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
        "-pt",
        "--prompt_type",
        type=conf.PromptType,
        choices=list(conf.PromptType),
        default=conf.PromptType.SIMPLE,
        help="Prompt type to be used",
        required=False
    )

    args = parser.parse_args()

    return args.root_dir, args.src_file, args.src_class, args.test_file, args.test_methods, args.prompt_type


def main() -> None:

    (root_dir, src_file, src_class, test_file, test_methods, prompt_type) = get_args()

    logging.info(f"Running with root_dir: {root_dir}, src_file: {src_file}, src_class: {src_class},"
                 f" test_file: {test_file}, test_methods: {test_methods}, prompt_type: {prompt_type}")

if __name__ == "__main__":
    main()
