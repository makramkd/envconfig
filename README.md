# envconfig

![](https://github.com/makramkd/envconfig/workflows/envconfig%20Python%20package/badge.svg)

`envconfig` is a simple but effective way to configure your Python application through environment variables.

Inspired by [kelseyhightower/envconfig](https://github.com/kelseyhightower/envconfig).

Features:
* Extremely simple setup,
* Zero third-party dependencies,
* Well tested,
* Well documented,
* Fun to use ;)

## Install

You can install `pyenvconfig` easily, using `pip`:

```
pip install pyenvconfig
```

## Quickstart

```python
import envconfig

class Config:
  # Declare two config variables with type string.
  aws_access_key_id: str
  aws_secret_access_key: str

  # Provide a default - envconfig uses the type that the attribute is initialized with
  # so you don't need to repeat yourself.
  aws_region = 'us-east-1'

  # HTTP config
  num_retries = 15
  retry_strategy: str
  timeout: int = 15  # seconds

# Create an instance of your config object and let envconfig process it!
config = Config()
envconfig.process(config)

# Access class attributes
aws_client = Client(
  access_key_id=config.aws_access_key_id,
  secret_access_key=config.aws_secret_access_key,
  region=config.aws_region,
)
```

## Development

### Cloning and Building

`envconfig` is written in Python 3.6 and is tested on Python 3.6 and above.

Simply check out the repository, create a `virtualenv`, and go to town!

```bash
git clone https://github.com/makramkd/envconfig  # or git@github.com:makramkd/envconfig.git if you prefer
cd envconfig
pyenv local 3.6.3  # ensure python 3.6
python -m venv .venv  # create venv
source .venv/bin/activate
pip install -r test_requirements.txt  # for coverage, flake8
```

You can install `envconfig` in your virtual environment by running:

```bash
python setup.py install
```

### Running unit tests and linter

All unit tests are built using the `unittest` module from the standard library.

```bash
python -m unittest discover tests/
```

Or, if you want a coverage report:

```bash
coverage run -m unittest discover tests
coverage report  # show coverage report on stdout
coverage html && open htmlcov/index.html  # show interactive coverage report in the browser
```

To run the linter:

```bash
./run_linter.sh
```

### Contributions

Contributing is easy. Create a pull request, add tests, and get it approved!
