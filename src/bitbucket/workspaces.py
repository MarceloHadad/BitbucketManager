import requests
import inspect
from config import base_url, workspace, headers

# List projects in a workspace
def list_projects_in_a_workspace():
    projects_in_workspace = []
    url = f'{base_url}workspaces/{workspace}/projects'

    response = requests.get(url, headers=headers)
    json_data = response.json()

    projects_in_workspace = json_data.get('values', [])

    print(f'[{inspect.stack()[0][3]}] {projects_in_workspace.__len__()} projects in workspace {workspace}')
    return projects_in_workspace
