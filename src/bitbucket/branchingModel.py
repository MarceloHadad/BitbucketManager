import requests
import inspect
from config import base_url, workspace, headers

# Get the branching model for a project
def get_the_branching_model_for_a_project(project_key):
    url = f'{base_url}workspaces/{workspace}/projects/{project_key}/branching-model'
    response = requests.get(url, headers=headers)
    json_data = response.json()

    print(f'[{inspect.stack()[0][3]}] Branching model for project {project_key}: {json_data}')

# Get the branching model for a repository
def get_the_branching_model_for_a_repository(repo_slug):
        url = f'{base_url}repositories/{workspace}/{repo_slug}/branching-model'
        response = requests.get(url, headers=headers)
        json_data = response.json()

        print(f'[{inspect.stack()[0][3]}] Branching model for repo {repo_slug}: {json_data}')
