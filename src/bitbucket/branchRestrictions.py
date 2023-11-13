import requests
import inspect
from config import base_url, workspace, headers

# List branch restrictions
def list_branch_restrictions(repo_slug):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/branch-restrictions'
    response = requests.get(url, headers=headers)
    json_data = response.json()

    print(f'[{inspect.stack()[0][3]}] Branch restrictions for repo {repo_slug}: {json_data}')

# Delete a branch restriction rule
def delete_a_branch_restriction_rule(repo_slug, id):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/branch-restrictions/{id}'
    response = requests.get(url, headers=headers)

    if response.status_code == 204:
        print(f'[{inspect.stack()[0][3]}] Branch restriction rule {id} deleted for repo {repo_slug}')

    else:
        print(f'[{inspect.stack()[0][3]}] Branch restriction rule {id} could not be deleted for repo {repo_slug}')
