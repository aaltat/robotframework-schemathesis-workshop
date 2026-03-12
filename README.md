# robotframework-schemathesis-workshop

Material work SchemathesisLibrary workshop

# Setup
## Requirements
Python LTS version is recommended: https://devguide.python.org/versions/ In time of this writing
Python 3.14 preferred.

Install uv: https://docs.astral.sh/uv/ or any other package manager that can
perform install from https://pypi.org/

Install Docker: https://www.docker.com/

Docker is needed for easy deployment of the test app

# Install

Clone the repository and run
```bash
uv sync
```

# Exercise
Task are divided to three different exercises. For exercise use max_example=3
in the library import, to speed up development.

The test app can be run with invoke (https://www.pyinvoke.org/):
```bash
invoke start-app
```
When command is completed, use browser to navigate to http://127.0.0.1/docs

## Exercise 1

Create a basic test which will use SchemathesisLibrary to read OpenAPI specification
from http://127.0.0.1/openapi.json and executes all test case. Some of the tests
will fail, which is OK.

## Exercise 2

Investigate the API documentation and SchemathesisLibrary to use realistic data from the database.

## Exercise 3

User api needs basic authentication, username is: joulu and password is: pukki, implement the authentication for the user api.
