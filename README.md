# Data Engineer Coding Challenge

## Goal
Creating a python lambda service that takes input form a SNS queue, calculates CTR for given input and writes the best performing click path into a PostgreSQL(-RDS) database.

[Task PDF(german)](./assets/task-german.pdf)

## Steps taken

First I extended on the local setup and added a postgres database and created a [SQL schema](./database/00-init.sql) to store the output in. Then I added the calculation logic into the lambda_handler function, parsing the sns message into [dataclasses](./src/ctr_entry.py) that handle the CTR related logic and added [tests](./tests/test_ctr_entry.py). After that added the [write operation to the database](./src/app.py#24). As last step I tried my luck with the [infrastructure setup in terraform](./infrastructure/main.tf)

## Requirements
- local setup:
    - `docker`
    - `docker-compose`
- unittests:
    - python3 >= 3.8 
    - installed [requirements.dev.txt](./tests/requirements.dev.txt)

## HowTo
Run `docker-compose up --build` in root directory.

## Known issues
- database might need more than 5 seconds to initalize, startupcheck in testing service is not implemented, might need to be increased in [curl-service](./curl-service/run.sh#4)