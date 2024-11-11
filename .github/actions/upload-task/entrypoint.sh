#!/bin/bash
set -euo pipefail

if [[ ! -d "$INPUT_PATH" ]]; then
    echo "::error::Provided path $INPUT_PATH is not a directory"
    exit 1
fi
zip -r task.zip "$INPUT_PATH" -x ".git/*" ".github/*"

python3 publish_task.py
if [[ "$INPUT_PUBLISH" == "true" ]]; then
    python3 publish_task.py
fi
