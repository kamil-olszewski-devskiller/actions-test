import os
import requests

TASKS_API = "https://api.stage-devskiller.com/tasks"

input_api_key = os.environ["INPUT_API_KEY"]
input_path = os.environ["INPUT_PATH"]

def validate_input_path():
    if not os.path.isfile(input_path) or not (input_path.endswith('.yaml') or input_path.endswith('.yml')):
        print("::error::PATH parameter is not a yaml file")        
        exit(1)

def import_file():
    print(f"::info::Importing the YAML file: {input_path}")
    with open(input_path, "rb") as f:
        response = requests.put(
            f"{TASKS_API}/yaml",
            data=f.read(),
            headers={"Content-Type": "application/yaml", "Devskiller-Api-Key": input_api_key},
        )

    if response.status_code not in [202, 422]:
        print(f"::error::Upload failed with status code: {response.status_code}, response: {response.text}")
        exit(1)

    return response

def write_summary(import_response):
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as f:
        body = import_response.json()

        markdown = ""
        if import_response.status_code == 422:
            markdown = "### Validation errors:\n"
            for violation in body.get('violations', []):
                markdown += f"- {violation}\n"
        elif import_response.status_code == 200:
            if body.get('created'):
                markdown += "### Created tasks:\n"
                for task in body.get('created', []):
                    markdown += f"- {task}\n"
            if body.get('updated'):
                markdown += "\n### Updated tasks:\n"
                for task in body.get('updated', []):
                    markdown += f"- {task}\n"

        f.write(markdown)


def main():
    validate_input_path()
    import_response = import_file()
    write_summary(import_response)

if __name__ == "__main__":
    main()