import os
import shutil
import requests
import time

TASKS_API = "https://api.stage-devskiller.com/tasks"
BUILD_CHECK_MAX_ATTEMPTS = 36

input_api_key = os.environ["INPUT_API_KEY"]
input_id = os.environ["INPUT_ID"]
input_path = os.environ["INPUT_PATH"]
input_publish = os.environ["INPUT_PUBLISH"]

def validate_input_path():
    if not os.path.isdir(input_path):
        print("::error::PATH parameter is not a directory")
        exit(1)

def create_zip_archive():
    shutil.make_archive("task", "zip", input_path)

def upload_task():
    print(f"::info::Uploading the task with ID: {input_id}")
    with open("task.zip", "rb") as f:
        upload_response = requests.put(
            f"{TASKS_API}/programming/{input_id}",
            data=f.read(),
            headers={"Content-Type": "application/zip", "Devskiller-Api-Key": input_api_key},
        )
    if upload_response.status_code != 202:
        print(f"::error::Upload failed with status code: {upload_response.status_code}, response: {upload_response.text}")
        exit(1)

def check_build_status():
    print("::info::Checking the build status")
    for _ in range(BUILD_CHECK_MAX_ATTEMPTS):
        status_response = requests.get(f"{TASKS_API}/{input_id}", headers={"Devskiller-Api-Key": input_api_key})       
        if status_response.status_code == 200:
            status_data = status_response.json()
            if status_data.get('buildStatus') is not None:
                print(f"::info::Build status is: {status_data.get('buildStatus')}")
                return status_data
            time.sleep(10)  
        else:
            print(f"::error::Build status check failed with status code: {status_response.status_code}, response: {status_response.text}")
            exit(1)
                 
    print("::error::Timeout waiting for build status")
    exit(1)

def format_summary_test_section(section_name, test_data):
    markdown = f"\n\n### {section_name}\n"
    for test_suite, tests in test_data.items():
        markdown += f"- {test_suite}:\n"
        for test_name, test_result in tests.items():
            markdown += f"  - {test_name}: **{'✅' if test_result == 'PASS' else '❌'}**\n"
    return markdown

def write_summary(status_data):
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as f:
        markdown = f"## Build Status: {status_data.get('buildStatus')} {'✅' if status_data.get('buildStatus') == 'TEST_FAILURE' else '❌'}\n---"
        markdown += format_summary_test_section("Candidate Tests", status_data.get('candidateTests', {}))
        markdown += format_summary_test_section("Verification Tests", status_data.get('verificationTests', {}))                   
        f.write(markdown)
        
def verify_build_status(status_data):
    if status_data.get('buildStatus') != 'TEST_FAILURE':
        print("::error::The initial state of the task should be compiling, but with broken tests")
        exit(1)

    if not status_data.get('verificationTests', {}):
        print("::error::You are missing the verification tests")
        exit(1)

def publish_task():
    print(f"::info::Publishing the task with ID: {input_id}")
    response = requests.post(
        f"{TASKS_API}/{input_id}/publish",
        headers={"Devskiller-Api-Key": input_api_key},
    )

    if response.status_code != 204:
        print(f"::error::Publication failed with status code: {response.status_code}, response: {response.text}")
        exit(1)

def main():
    validate_input_path()
    create_zip_archive()
    upload_task()
    build_status = check_build_status()
    write_summary(build_status)
    verify_build_status(build_status)
    if input_publish:
        publish_task()

if __name__ == "__main__":
    main()