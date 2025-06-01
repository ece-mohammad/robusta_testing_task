# Swag labs

Automation testing for swag-labs website using Pytest and Selenium.

## Installation

1. clone repo

    ```
    git clone [repo_url] swag_labs
    ```

2. go to repo directory

    ```
    cd swag_labs
    ```

3. create virtual environment

    ```
    uv venv
    ```

4. activate virtual environment

    ```
    . ./.venv/bin/activate
    ```

5. install required packages

    ```
    uv pip install -r requirements.txt
    ```

## Configurations

`.env.dist` file contains configurations required to run the tets as environment variables:

- `BROWSER`: browser used to run the tests. Currently the tests are supported only for firefox and chrome.
- `DATA_END_POINT`: REST API endpoint to get user info, the test uses a [fake JSON server](https://my-json-server.typicode.com/)

## Run tests

just call `pytest` in the root directory

```
pytest
```
