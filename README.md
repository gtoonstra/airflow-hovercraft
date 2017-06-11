# airflow-hovercraft
A reference implementation of hooks and operators for airflow

[![Build Status](https://travis-ci.org/gtoonstra/airflow-hovercraft.svg)](https://travis-ci.org/gtoonstra/airflow-hovercraft)
[![Coverage Status](https://coveralls.io/repos/github/gtoonstra/airflow-hovercraft/badge.svg?branch=master)](https://coveralls.io/github/gtoonstra/airflow-hovercraft?branch=master)
[![Requirements Status](https://requires.io/github/gtoonstra/airflow-hovercraft/requirements.svg?branch=master)](https://requires.io/github/gtoonstra/airflow-hovercraft/requirements/?branch=master)

### How to run all tests

Create and activate a virtual env:

```
python3 -m venv env
source env/bin/activate
```

Install the CI requirements:

```
cd scripts/ci
pip install -r requirements.txt
```

Run the tests from the root directory:

```
cd ../..
./run_unit_tests.sh
```

Run the "behave" tests:

```
./run_behave.sh
```


### Use in a production system

Install the "requirements.txt"  from the root directory:

```
cd /
pip install -r requirements.txt
```

Then install the project through setup.py:

```
python setup.py install
```
