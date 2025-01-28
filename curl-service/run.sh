#!/bin/sh

echo "Waiting for database"
sleep 5
echo "Sending test events..."


curl -X POST -d "@/app/request1.json" --url http://ab-test-lambda:8080/2015-03-31/functions/function/invocations -H "Content-Type: application/json"
sleep 1
curl -X POST -d "@/app/request2.json" --url http://ab-test-lambda:8080/2015-03-31/functions/function/invocations -H "Content-Type: application/json"
sleep 1
curl -X POST -d "@/app/request3.json" --url http://ab-test-lambda:8080/2015-03-31/functions/function/invocations -H "Content-Type: application/json"
sleep 1



