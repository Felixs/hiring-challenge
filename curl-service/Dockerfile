FROM curlimages/curl:latest

WORKDIR /app/

COPY ./run.sh .
COPY ./sample-requests/*.json .

CMD ["sh", "run.sh"]
