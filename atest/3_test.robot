*** Settings ***
Library             SchemathesisLibrary
...                     url=http://127.0.0.1/openapi.json
...                     max_examples=3
...                     hook=${CURDIR}/hook.py
...                     auth=${CURDIR}/AuthExtension.py

Test Template       Wrapper


*** Test Cases ***
Example
    Log    This is an dummy case for RF, will be automatically deleted.


*** Keywords ***
Wrapper
    [Arguments]    ${case}
    Call And Validate    ${case}
