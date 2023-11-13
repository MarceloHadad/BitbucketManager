import requests
import inspect
from config import base_url, workspace, headers

# List the default reviewers in a project
def list_the_default_reviewers_in_a_project(project_key):
    url = f'{base_url}workspaces/{workspace}/projects/{project_key}/default-reviewers'
    response = requests.get(url, headers=headers)
    json_data = response.json()

    print(f'[{inspect.stack()[0][3]}] Default reviewers for project {project_key}:')
    for reviewer in json_data['values']:
        print(f'[{inspect.stack()[0][3]}] {reviewer}')

# Add the specific user as a default reviewer for the project
def add_the_specific_user_as_a_default_reviewer_for_the_project(project_key, selected_user_id):
    url = f'{base_url}workspaces/{workspace}/projects/{project_key}/default-reviewers/{selected_user_id}'
    payload = ""

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201:
        print(f'[{inspect.stack()[0][3]}] Error adding user {selected_user_id} as a default reviewer for project {project_key}')
    else:
        print(f'[{inspect.stack()[0][3]}] User {selected_user_id} added as a default reviewer for project {project_key}')

# Delete an explicit user permission for a project
def delete_an_explicit_user_permission_for_a_project(project_key, selected_user_id):
    url = f'{base_url}repositories/{workspace}/{project_key}/permissions-config/users/{selected_user_id}'

    response = requests.delete(url, headers=headers)   
    if response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error deleting user {selected_user_id} from repo {project_key}')
    else:
        print(f'[{inspect.stack()[0][3]}] User {selected_user_id} deleted from repo {project_key}')
