# for local testing

FROM amazon/aws-lambda-python:3.12
COPY ./src/requirements.txt /data/src/
RUN pip3 install -r /data/src/requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN mkdir -p ${LAMBDA_TASK_ROOT}/src
COPY ./src/ ${LAMBDA_TASK_ROOT}/src

CMD ["src.app.lambda_handler"]