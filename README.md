# ChekProp
ChekProp is an LLM-based tool for generating property-based tests for
cyber physical systems.

## How to use
To use ChekProp, you should have `poetry` installed. ChekProp is tested with Python 3.11.

1. Clone ChekProp `git clone git@github.com:khesoem/ChekProp.git` and `cd ChekProp`.
2. Install ChekProp dependencies `poetry install`.
3. Add two environment variables:
    - `export OPENROUTER_API_KEY={your-openrouter-api-key}`. Note that you should have an [openrouter API key to use ChekProp](https://openrouter.ai/).
    - `export PYTHONUNBUFFERED=1`.
4. Run ChekProp as follows:

```
python main.py -r {path-to-project-root} -sf {path-to-source-file} -sc {source-class} -tf {path-to-unittests-file} -tm {path-to-test-methods} -op {path-to-output-dir}`.
```
For example:
```
-r {absolute-path-to-chekprop}/examples/gpiozero/apps/app_1 -sf src/laser_tripwire.py -sc LaserTripwire -tf test/test_laser_tripwire_units.py -tm test_prints_when_dark -op generated_tests
```
For this example, the generated test and its output will be saved at `examples/gpiozero/apps/app_1/generated_tests/` directory. Note that previous experiment results, which used the `gemini-2.0-flash-lite-preview-02-05:free` model are already saved in that directory. New generated tests will be saved in new test files.

As `gemini-2.0-flash-lite-preview-02-05:free'` is no longer available on OpenRouter, ChekProp now uses `qwen/qwen3-coder:free` as the default model.