# DevSkiller TalentScore - Import tasks from YAML

This GitHub Action uploads custom MCQ/Essay/CodeGaps tasks to the DevSkiller TalentScore platform. It allows you to easily integrate the import from YAML process into your CI/CD pipeline.

## Inputs

### `api_key`
**Required**: The TalentScore API key. This key is needed to authenticate the upload request.

### `path`
**Required**: The path to the programming task directory that contains the task source code to upload.

## Example

```yaml
name: Sample YAML import

on:
  push:
    branches:
      - master

jobs:
  upload-task:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - uses: Devskiller/talentscore-import-yaml-action@v1.0.0
        with:
          api_key: ${{ secrets.TALENTSCORE_API_KEY }}
          path: ./java-tasks.yml
```