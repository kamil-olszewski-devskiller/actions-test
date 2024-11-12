# DevSkiller TalentScore - Upload task action

This GitHub Action uploads custom programming tasks to the DevSkiller TalentScore platform. It allows you to easily integrate the upload process into your CI/CD pipeline.

## Inputs

### `api_key`
**Required**: The TalentScore API key. This key is needed to authenticate the upload request.

### `id`
**Required**: The ID of the programming task you want to modify on the TalentScore platform.

### `path`
**Required**: The path to the programming task directory that contains the task source code to upload.

### `publish`
**Optional**: If set to `true` (default), the task will be published automatically after a successful build.

## Example

```yaml
name: Sample task upload

on:
  push:
    branches:
      - master

jobs:
  upload-task:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - uses: devskiller/upload-task@1
        with:
          api_key: ${{ secrets.TALENTSCORE_API_KEY }}
          id: fe3217a6-e085-47dd-afff-025be5355d87
          path: ./src
```
