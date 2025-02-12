# ChekShe
ChekShe is an LLM-based tool for generating property-based tests for
cyber physical systems.

## How to use
To use ChekShe, you should have `poetry` installed.

1. Clone ChekShe `git clone git@github.com:khesoem/ChekShe.git` and `cd ChekShe`.
2. Install ChekShe dependencies `poetry install`.
3. Run ChekShe:

```
python main.py -r {path-to-project-root} -sf {path-to-source-file} -sc {source-class} -tf {path-to-unittests-file} -tm {path-to-test-methods} -op {path-to-output-dir}`.
```
For example:
```
-r {absolute-path-to-chekshe}/examples/gpiozero/apps/app_1 -sf src/laser_tripwire.py -sc LaserTripwire -tf test/test_laser_tripwire_units.py -tm test_prints_when_dark -op generated_tests
```
The generated test and its output will be saved at `generated_tests` directory.