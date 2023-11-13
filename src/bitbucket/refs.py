import requests
import json
import inspect
from config import base_url, workspace, headers

# List branches and tags
def list_branches_and_tags(repo_slug):
    branches_and_tags_in_repo = []
    url = f'{base_url}repositories/{workspace}/{repo_slug}/refs'

    while True:
        response = requests.get(url, headers=headers)
        branches_and_tags_in_repo.extend(response.json().get('values', []))
        next_url = response.json().get('next')
        if next_url is None:
            break
        url = next_url

    print(f'[{inspect.stack()[0][3]}] {branches_and_tags_in_repo.__len__()} branches and tags in repo {repo_slug}')
    return branches_and_tags_in_repo

# Create a branch
def create_a_branch(repo_slug, branch_name, target):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/refs/branches'
    headers.update({'Content-Type': 'application/json'})

    payload = json.dumps({
        "type": "branch",
        "name": branch_name,
        "target": target
        })

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 201:
        print(f'[{inspect.stack()[0][3]}] Error creating branch {branch_name} in repo {repo_slug}')
        print(f'[{inspect.stack()[0][3]}] {response.text}')
        return False
    else:
        print(f'[{inspect.stack()[0][3]}] Branch {branch_name} created in repo {repo_slug}')
        return get_a_branch(repo_slug, branch_name)
    
# Get a branch
def get_a_branch(repo_slug, branch_name):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/refs/branches/{branch_name}'
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'[{inspect.stack()[0][3]}] Error getting branch {branch_name} in repo {repo_slug}')
        print(f'[{inspect.stack()[0][3]}] {response.text}')
        return False
    else:
        print(f'[{inspect.stack()[0][3]}] Branch {branch_name} in repo {repo_slug} exists')
        return response.json()

# Delete a branch
def delete_a_branch(repo_slug, branch_name):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/refs/branches/{branch_name}'

    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error deleting branch {branch_name} in repo {repo_slug}')
        print(f'[{inspect.stack()[0][3]}] {response.text}')
        return False
    else:
        print(f'[{inspect.stack()[0][3]}] Branch {branch_name} deleted in repo {repo_slug}')
        return True
