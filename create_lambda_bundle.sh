#!/bin/bash

OUTPUT_FILE="./dist/lambda_ctr_function.zip"

# Remove the existing zip file if it exists
if [ -f "$OUTPUT_FILE" ]; then
    rm "$OUTPUT_FILE"
fi

# Create a new zip file with the contents of the source directory
zip -r "$OUTPUT_FILE" "./src/" 

echo "Bundling complete: $OUTPUT_FILE"